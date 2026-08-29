<!-- # IDS Rule-Based Engine

Cybersecurity-developer module of the group IDS project. Captures live
traffic with Scapy, runs it through six detection rules, and forwards any
attack it finds to the FastAPI backend.

## Setup

```bash
pip install -r requirements.txt
sudo python3 main.py          # raw packet capture needs root/admin
sudo python3 main.py eth0     # or target a specific interface
```

## Architecture

## Rules

### Rule 1 — Ping Flood
**Trigger:** one source IP sends `PING_FLOOD_COUNT` (default 50) ICMP packets
within `PING_FLOOD_WINDOW` (default 1s).
**Why:** a flood of ICMP echo requests in a tight window is the classic
ping-flood DoS signature.
**State:** a per-IP deque of ICMP timestamps, pruned to the current window
on every packet.

### Rule 2 — Port Scan
**Trigger:** one source IP touches `PORT_SCAN_COUNT` (default 30) distinct
destination ports within `PORT_SCAN_WINDOW` (default 10s).
**Why:** legitimate clients hit one or two ports; scanners sweep many in a
short burst.
**State:** a per-IP dict of `{port: last_seen_timestamp}`, with stale ports
dropped each time.

### Rule 3 — SYN Flood
**Trigger:** one source IP sends `SYN_FLOOD_COUNT` (default 100) SYN packets
**without** the ACK flag (i.e. the handshake never completes from that
side) within `SYN_FLOOD_WINDOW` (default 5s).
**Why:** SYN flood attacks open many half-connections and never finish the
3-way handshake, exhausting the target's connection table.
**Note:** this is a simplified heuristic (raw SYN-without-ACK volume) rather
than full per-connection handshake state tracking — good enough for a demo
IDS, worth calling out if asked in a viva/review.

### Rule 4 — Blacklisted IP
**Trigger:** the packet's source IP appears in `config.BLACKLISTED_IPS`.
**Why:** known-bad IPs (from threat feeds, prior incidents, etc.) should be
flagged on sight, independent of behavior.
**State:** none — a direct set lookup.

### Rule 5 — Malformed Packet
**Trigger:** a TTL of 0 or less, or a TCP packet with a contradictory flag
combination (SYN+FIN or SYN+RST both set — flag combinations that should
never legitimately co-occur).
**Why:** malformed headers are often used to evade firewalls/IDS or crash
poorly-written network stacks.

### Rule 6 — Large Packet
**Trigger:** `packet_size` exceeds `LARGE_PACKET_THRESHOLD` (default 1500
bytes, the standard Ethernet MTU).
**Why:** oversized packets can indicate fragmentation abuse or
exfiltration attempts; the threshold is configurable per network.

## Detection output format

Every rule that fires returns an `Attack`, which `api.py` posts to the
backend as:

```json
{
  "attack": "Ping Flood",
  "severity": "High",
  "source_ip": "192.168.1.10",
  "timestamp": "2026-07-29T16:43:57.123456",
  "description": "Exceeded ICMP threshold: 50+ packets within 1s"
}
```

## Testing without live attack traffic

You don't need a real botnet to test this. From a second machine (or a
loopback test), you can simulate each rule with Scapy one-liners, e.g.:

```python
from scapy.all import send, IP, ICMP
# Ping flood simulation
send(IP(dst="TARGET_IP")/ICMP(), count=60, inter=0.01)
```

Adjust thresholds in `config.py` down temporarily (e.g. `PING_FLOOD_COUNT =
5`) while testing locally so you don't need to generate huge traffic
volumes to see an alert fire. -->