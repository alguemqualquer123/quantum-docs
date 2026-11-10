---
description: Run two independent Quantum runtime windows from the editor for multiplayer testing.
---

# Network Play

**Scene → Network Play** opens a focused test panel for local multiplayer. It
launches the same saved project twice: once as a server and once as a client.

## Controls

| Field | Meaning |
| --- | --- |
| Scene entry | Lua entry used by `quantum-engine` |
| Client address | Server address used by the client window |
| Session token | Optional shared HMAC token; passed through the child environment |
| Port | UDP port shared by the two players |
| Window size | Initial size for both runtime windows |

Use **Launch server window** and **Launch client window** for independent
control, or **Launch both windows** for the normal local test. Each child shows
its PID and exit state. The panel prevents duplicate launches and freezes the
session parameters while either process is active.

The panel stores the project path rather than a dangling project pointer,
rolls back the server when the client launch fails, and cleans up only child
processes it created. Closing the editor does not modify project scenes.

## Production boundary

Network Play is a local two-process harness. It does not replace matchmaking,
lobby services, NAT traversal, or an authoritative gameplay model for a shipped
game. See [Networking](../manual/networking.md) for the runtime contract.

