---
description: UDP networking, authentication, replication, reconnection, and local multiplayer testing in Quantum.
---

# Networking

Quantum's runtime networking is a versioned UDP system built around
`NetworkProtocol` and `NetworkSystem`. It is designed for authoritative server
play, with reliable, unreliable, and snapshot channels in one transport.

## Current capabilities

- QNET version 1 framing with `Hello`, `HelloAck`, `Data`, `Ack`, `Snapshot`,
  `Unreliable`, `SnapshotCompressed`, `InterestUpdate`, and additive
  `ReplicationPolicy`, `LobbyQuery`, `LobbyAdvertisement`, authenticated
  `LobbyReservationRequest`/`LobbyReservationResponse`, and relay control
packets (`RelayRegister`/`RelayJoin`/`RelayReady`/`RelayHeartbeat`).
- HMAC-SHA256 authentication for every datagram, endpoint pinning after the
  handshake, tamper rejection, and rate/size limits.
- Bounded multi-peer server admission (default 16 peers, configurable with
  `NetworkSystem:setMaxPeers`), distinct server-assigned `peerId` values and
  `getConnectedPeerCount()`, with per-peer reliable ordering/retry state.
- Server broadcast of application messages and authoritative snapshots, with
  each peer's interest center/radius/group applied independently; clients still
  use prediction/reconciliation, interpolation, timeout, and reconnect handling.
- Interest center, radius, group filtering, owner policy, replication metrics,
  RTT, loss, queue depth, malformed and unauthorized packet counters.
- LAN lobby discovery over the same UDP port. `NetworkSystem::discoverLan` uses
  broadcast by default (or an explicit IPv4 address), and authenticated servers
  only answer queries carrying the matching HMAC token. Discovery reports the
  server name, map, build ID, game port, current peers, and maximum peers
  without creating a gameplay session or consuming a peer slot.

Game-specific reliable commands can use `NetworkSystem::registerServerMessageSchema`
to enforce a current version, maximum payload size, and a validator that receives
the authenticated `peerId` before a command reaches gameplay. Invalid envelopes
are acknowledged to prevent retry storms but are dropped and counted as
unauthorized; legacy unversioned payloads remain compatible.

The server is authoritative for snapshots. The transport now provides bounded
peer admission, LAN room discovery and short-lived authenticated room
reservations. `NetworkSystem::reserveLan` returns a reservation ID; pass it to
`startClient` so the reserved client can consume the slot before the timeout.
Retries reuse the same reservation nonce, while different clients behind one NAT
can reserve distinct slots. An expired or unknown reservation ID is rejected at
handshake time, so the client must reserve again.

For the dedicated-server/NAT fallback path, the release also ships
`quantum-network-relay`. It authenticates room registration/join control
packets with its deployment token, allocates a virtual UDP port per participant
and forwards opaque QNET datagrams. Gameplay HMAC remains end-to-end between
the server and clients; the relay does not rewrite gameplay messages.
The relay bounds each room and applies independent flood limits: 2,400 control
packets/256 KiB per second globally and 1,200 opaque packets/2 MiB per second per
virtual destination, with oversized datagrams counted before rejection.
It caps the directory at 256 rooms, expires idle host/member leases, removes
expired indices from room membership, and reuses their virtual-port slots. Once
the host lease expires, a new authenticated `RelayRegister` can take ownership
of the room; existing clients receive the replacement virtual peer port on the
next heartbeat.
After registration/join, each runtime sends the authenticated `RelayHeartbeat`
every ten seconds, keeping an otherwise idle participant alive. The relay logs
accepted and rejected heartbeat counters when it stops.
ICE/STUN/TURN, hosted matchmaking and multi-region failover remain deployment
services around this relay.

```powershell
$env:QUANTUM_NETWORK_TOKEN = "game-secret"
$env:QUANTUM_RELAY_TOKEN = "relay-secret"
build\Release\quantum-network-relay.exe --port 39279 `
    --token $env:QUANTUM_RELAY_TOKEN
quantum-engine.exe --project . --network-relay-server 127.0.0.1 39279 room-a `
    --network-token-env QUANTUM_NETWORK_TOKEN `
    --network-relay-token-env QUANTUM_RELAY_TOKEN
quantum-engine.exe --project . --network-relay-client 127.0.0.1 39279 room-a `
    --network-token-env QUANTUM_NETWORK_TOKEN `
    --network-relay-token-env QUANTUM_RELAY_TOKEN
```

The deterministic integration check starts the relay, one real headless server
and two simultaneous real headless clients:

```powershell
python scripts/network-relay-smoke.py --root . --config Release
```

## Gameplay authority

`NetworkComponent.ownerId` identifies the peer allowed to author a replicated
entity. The server has authority for its scene; a client gains authority only
after its non-zero `ownerId` matches `NetworkSystem:getLocalPeerId()`.
Prediction requests for another peer's entity are ignored, and gameplay can
query the same rule before accepting local input:

```lua
local network = scene:getNetworkSystem()
if network:hasEntityAuthority(playerEntity) then
    network:setPredictionVelocity(playerEntity, velocity)
end
```

The authority check is also covered by the Release `quantum-network-smoke`
test. It does not replace server-side validation of game-specific commands or
a lobby that assigns ownership.

The policy is persistent in both places that carry network state: editor YAML
and the `QNETECS3` save snapshot. The snapshot serializer is schema 2 and still
accepts schema 1 payloads, so old saves retain their `replicateTransform` value
without inventing ownership data.

The runtime also exposes a read-only catalog of registered component serializers
(`NetworkSystem::getReplicatedComponentCatalog()`), containing deterministic names
and schema versions but no callbacks. The MSVC serialization smoke checks that the
catalog is unique and complete for the built-in registrations.

During live replication the server sends an additive `ReplicationPolicy` packet
next to each transform snapshot. New clients apply it before evaluating local
authority; older clients can ignore that packet and continue using the legacy
transform stream.

## Authenticated local run

Keep the token out of source control and out of process arguments:

```powershell
$env:QUANTUM_NETWORK_TOKEN = "replace-with-a-secret"
quantum-engine.exe --project . --network-server 39179 `
    --network-token-env QUANTUM_NETWORK_TOKEN
quantum-engine.exe --project . --network-client 127.0.0.1 39179 `
    --network-token-env QUANTUM_NETWORK_TOKEN
```

The legacy `--network-token TOKEN` option remains for local scripts. The editor's
Network Play window uses the environment form and creates two independent runtime
windows.

The relay smoke also has a deterministic takeover mode:

```powershell
python scripts/network-relay-smoke.py --root . --config Release --failover
```

It uses the production relay-control packet format, stops the original host,
waits for its authenticated lease to expire while the client heartbeat remains
active, and verifies that a replacement host registers in the same room.

## Testing two players in the editor

Open **Scene → Network Play**. Choose the scene entry, port, client address,
window size, and optional token, then select **Launch both windows**. The panel
shows each child PID and exit code, prevents configuration changes while a
session is active, rolls back the server if the client cannot launch, and only
stops processes created by that panel.

For a deterministic headless soak:

```powershell
build\Debug\quantum-network-smoke.exe --reconnect-soak 12000 3 20 35
```

The soak exercises server restart, queued reliable messages, retransmission,
simulated loss/reordering, and peer identity restoration. Its active and outage
windows include explicit margin above the 750 ms client timeout and asynchronous
server startup, making the final HelloAck deterministic under normal host load.

