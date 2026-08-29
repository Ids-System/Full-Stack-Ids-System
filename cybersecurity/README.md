# 🔍 Cybersecurity — IDS Rule-Based Detection Engine

The cybersecurity module of the Full-Stack IDS System. It sniffs live network traffic using Scapy and runs each captured packet through six detection rules. When an attack is detected, it sends an alert to the FastAPI backend via HTTP.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3** | Core language |
| **Scapy** | Live packet capture and parsing |
| **Requests** | HTTP client to forward alerts to backend |
| **python-dotenv** | Loading environment variables |

## 📁 Project Structure

```
cybersecurity/
├── main.py              # Entry point — starts the packet sniffer
├── sniffer.py           # Scapy sniffer — captures packets and dispatches them
├── detector.py          # Detection engine — 6 rule functions
├── api.py               # HTTP client — sends Attack objects to the backend
├── models.py            # Attack dataclass (the alert payload)
├── config.py            # Thresholds, blacklists, and backend URL
├── traffic_generator.py # Test utility — simulates attack traffic
└── requirements.txt     # Python dependencies
```

## ⚙️ Setup & Installation

### 1. Create a Virtual Environment
```bash
cd cybersecurity
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the `cybersecurity/` directory:

```env
ENGINE_KEY=your_engine_api_key_here
```

> ⚠️ This must match the `ENGINE_KEY` set in the backend's `.env` — it authenticates the engine's requests to the API.

### 4. Run the Engine

> **Root privileges are required** for raw packet capture.

```bash
# Auto-detect the default network interface
sudo python3 main.py

# Target a specific interface (e.g., eth0, wlan0)
sudo python3 main.py eth0
```

## 🧪 Testing Without Live Attack Traffic

You do **not** need a real attack or a botnet to test the engine. Use the included traffic generator:

```bash
# From a second terminal (inside the venv)
python3 traffic_generator.py
```

You can also use Scapy one-liners from another machine or a loopback:

```python
from scapy.all import send, IP, ICMP

# Simulate a Ping Flood
send(IP(dst="TARGET_IP") / ICMP(), count=60, inter=0.01)
```

**Tip:** Temporarily lower thresholds in `config.py` to trigger rules quickly during local testing:
```python
PING_FLOOD_COUNT = 5
PORT_SCAN_COUNT = 5
SYN_FLOOD_COUNT = 10
```

## 🔗 How It Works

```
Network Interface
      │
      ▼
  sniffer.py          ← Scapy sniff() loop
      │ parsed Packet
      ▼
  detector.py         ← runs all 6 rules
      │ Attack object (if rule fires)
      ▼
   api.py             ← HTTP POST to backend /engine/report
      │
      ▼
  Backend API         ← stores alert and broadcasts via WebSocket
```

Every captured packet is parsed into a `Packet` dataclass and passed through all 6 rules. If any rule fires, the engine calls `api.send_alert()`, which POSTs the alert to the backend with the `X-Engine-Key` header for authentication.

## 🛡️ Detection Rules

### Rule 1 — Ping Flood
- **Trigger:** A single source IP sends ≥ `PING_FLOOD_COUNT` (default: **50**) ICMP packets within `PING_FLOOD_WINDOW` (default: **1 second**).
- **Severity:** HIGH
- **Why:** A burst of ICMP echo requests in a tight window is the classic ping-flood DoS signature.
- **State:** Per-IP deque of ICMP timestamps, pruned to the current window on every packet.

### Rule 2 — Port Scan
- **Trigger:** A single source IP touches ≥ `PORT_SCAN_COUNT` (default: **30**) distinct destination ports within `PORT_SCAN_WINDOW` (default: **10 seconds**).
- **Severity:** HIGH
- **Why:** Legitimate clients hit one or two ports; scanners sweep many in a short burst.
- **State:** Per-IP dict of `{port: last_seen_timestamp}` with stale ports pruned on each packet.

### Rule 3 — SYN Flood
- **Trigger:** A single source IP sends ≥ `SYN_FLOOD_COUNT` (default: **100**) SYN-only packets (no ACK flag) within `SYN_FLOOD_WINDOW` (default: **5 seconds**).
- **Severity:** CRITICAL
- **Why:** SYN flood attacks open many half-connections without completing the TCP 3-way handshake, exhausting the target's connection table.
- **Note:** This is a simplified heuristic (raw SYN-without-ACK volume), not full per-connection state tracking.

### Rule 4 — Blacklisted IP
- **Trigger:** The packet's source IP appears in `config.BLACKLISTED_IPS`.
- **Severity:** HIGH
- **Why:** Known-bad IPs should be flagged on sight, independent of behavior.
- **State:** None — a direct `set` lookup. Add IPs to `BLACKLISTED_IPS` in `config.py`.

### Rule 5 — Malformed Packet
- **Trigger:**
  - TTL value ≤ 0, **or**
  - TCP packet with contradictory flag combination (SYN+FIN or SYN+RST).
- **Severity:** MEDIUM
- **Why:** Malformed headers are commonly used to evade firewalls/IDS or crash vulnerable network stacks.

### Rule 6 — Large Packet
- **Trigger:** Packet size exceeds `LARGE_PACKET_THRESHOLD` (default: **1500 bytes**, the standard Ethernet MTU).
- **Severity:** LOW
- **Why:** Oversized packets can indicate fragmentation abuse or data exfiltration. Threshold is configurable per network.

## 📤 Alert Payload Format

When a rule fires, the engine sends the following JSON to `POST /engine/report`:

```json
{
  "attack": "PING FLOOD ATTACK",
  "severity": "HIGH",
  "source_ip": "192.168.1.10",
  "destination_ip": "192.168.1.1",
  "protocol": "ICMP",
  "port": 0,
  "timestamp": "2026-07-29T16:43:57.123456",
  "description": "Exceeded ICMP threshold: 50+ packets within 1s"
}
```

## ⚙️ Configuration Reference (`config.py`)

| Variable | Default | Description |
|---|---|---|
| `API_URL` | `http://127.0.0.1:8000/engine/report` | Backend endpoint to POST alerts |
| `API_TIMEOUT` | `3` | HTTP request timeout in seconds |
| `PING_FLOOD_COUNT` | `50` | ICMP packets threshold for Rule 1 |
| `PING_FLOOD_WINDOW` | `1` | Time window in seconds for Rule 1 |
| `PORT_SCAN_COUNT` | `30` | Distinct ports threshold for Rule 2 |
| `PORT_SCAN_WINDOW` | `10` | Time window in seconds for Rule 2 |
| `SYN_FLOOD_COUNT` | `100` | SYN packets threshold for Rule 3 |
| `SYN_FLOOD_WINDOW` | `5` | Time window in seconds for Rule 3 |
| `BLACKLISTED_IPS` | `{"1.2.3.4", "5.6.7.8"}` | Set of blocked source IPs for Rule 4 |
| `LARGE_PACKET_THRESHOLD` | `1500` | Packet size threshold in bytes for Rule 6 |
| `LOG_FILE` | `logs/ids_engine.log` | Log file path |

## 📋 Logging

All alert sends and API errors are written to `logs/ids_engine.log`. The log includes timestamps, severity level, and alert payloads. If the backend is unreachable, alerts are logged locally instead of being lost.