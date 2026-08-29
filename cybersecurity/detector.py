import config
import models
import api
from datetime import datetime
from collections import defaultdict, deque

icmp_hits = defaultdict(deque)    # {ip: deque of timestamps}
ports_seen = defaultdict(dict)   # {ip: {port: last_seen_timestamp}}
syn_hits = defaultdict(deque) 

def _prune_deque(dq, window_seconds, now):
    while dq and now - dq[0] > window_seconds:
        dq.popleft()

def _build_attack(packet, attack_name, severity, description):
    # Report.port is a required int - fall back to 0 for packets with no port
    # (ICMP, ARP) since the schema has no Optional/None allowance.
    port = packet.Destination_Port if packet.Destination_Port is not None else 0
    return models.Attack(
        attack=attack_name,
        severity=severity,
        source_ip=packet.Source_IP,
        destination_ip=packet.Destination_IP,
        protocol=packet.Protocol,
        port=port,
        timestamp=datetime.now().isoformat(),
        description=description,
    )

#Rule No 1: PING FLOOD
def check_ping_flood(packet):
    if packet.Protocol != "ICMP":
        return None

    hits = icmp_hits[packet.Source_IP]
    hits.append(packet.Time_Stamps)
    _prune_deque(hits, config.PING_FLOOD_WINDOW, packet.Time_Stamps)

    if len(hits) >= config.PING_FLOOD_COUNT:
        hits.clear()
        return _build_attack(
            packet,
            "PING FLOOD ATTACK",
            "HIGH",
            f"Exceeded ICMP threshold: {config.PING_FLOOD_COUNT} + packets "
            f"Within {config.PING_FLOOD_WINDOW}s",
        )
    return None

#Rule No 2: PORT SCAN
def check_port_scan(packet):
    if packet.Destination_Port is None:
        return None

    now = packet.Time_Stamps
    ports = ports_seen[packet.Source_IP]
    ports[packet.Destination_Port] = packet.Time_Stamps

    stale_ports = []
    for port, last_seen in ports.items():
        if now - last_seen > config.PORT_SCAN_WINDOW:
            stale_ports.append(port)

    for port in stale_ports:
        del ports[port]

    if len(ports) >= config.PORT_SCAN_COUNT:
        ports.clear()
        return _build_attack(
            packet,
            "PORTS SCAN",
            "HIGH",
            f"Accessed {config.PORT_SCAN_COUNT}+ Distinct Ports Within "
            f"{config.PORT_SCAN_WINDOW}s",
        )
    return None

#Rule No 3: SYN FLOOD
def check_syn_flood(packet):
    if packet.Protocol != "TCP" or not packet.TCP_Flags:
        return None

    Flags = packet.TCP_Flags
    is_syn_only = "S" in Flags and "A" not in Flags
    if not is_syn_only:
        return None

    hits = syn_hits[packet.Source_IP]
    hits.append(packet.Time_Stamps)
    _prune_deque(hits, config.SYN_FLOOD_WINDOW, packet.Time_Stamps)

    if len(hits) >= config.SYN_FLOOD_COUNT:
        hits.clear()
        return _build_attack(
            packet,
            "SYN FLOOD ATTACK",
            "Critical",
            f"{config.SYN_FLOOD_COUNT}+ SYN Packets without completed "
            f"handshake within {config.SYN_FLOOD_WINDOW}s",
        )
    return None

#Rule No 4: Blacklisted IP
def check_blacklisted_ip(packet):
    if packet.Source_IP in config.BLACKLISTED_IPS:
        return _build_attack(
            packet,
            "BLACKLISTED IP",
            "High",
            "Packets received from a Blacklisted Source IP ",
        )
    return None

#Rule No 5: Malformed Packet and Invalid TCP Header
def check_malformed_packet(packet):
    if packet.TTL is not None and packet.TTL <= 0:
        return _build_attack(
            packet,
            "MALFORMED PACKET",
            "Medium",
            "Invalid TTL value (<= 0)",
        )
    if packet.Protocol == "TCP" and packet.TCP_Flags:
        Flags = packet.TCP_Flags
        if ("S" in Flags and "F" in Flags) or ("S" in Flags and "R" in Flags):
            return _build_attack(
                packet,
                "MALFORMED PACKET",
                "Medium",
                f"Contradictory TCP flags in header: {Flags}",
            )
    return None

#Rule No 6: Large Packet Size
def check_large_packet(packet):
    if packet.Packet_Size > config.LARGE_PACKET_THRESHOLD:
        return _build_attack(
            packet,
            "LARGE PACKET",
            "Low",
            f"Packet size {packet.Packet_Size} bytes exceeds threshold of "
            f"{config.LARGE_PACKET_THRESHOLD} bytes",
        )
    return None

#Run rules on every packet
RULES = [
    check_blacklisted_ip,
    check_malformed_packet,
    check_ping_flood,
    check_port_scan,
    check_syn_flood,
    check_large_packet
]

def process_packet(packet):
    for rule in RULES:
        result = rule(packet)
        if result is not None:
            print(f"[ALERT] {result.attack} <- {result.source_ip} | {result.description}")
            api.send_alert(result)