"""
Traffic Generator - for testing the IDS Rule-Based Engine locally.

IMPORTANT:
Only ever point this at a target you own or control:
  - 127.0.0.1 (localhost)          <- default, safest
  - a VM / second machine on your own LAN
  - an isolated lab network you set up yourself

Never run this against a real website, public IP, or any system you
don't have explicit permission to test. Flood-style traffic against
third-party infrastructure is a denial-of-service attack, full stop,
regardless of intent.

Usage:
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule all
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule ping_flood
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule port_scan
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule syn_flood
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule malformed
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule large_packet
    sudo python3 traffic_generator.py --target 127.0.0.1 --rule blacklisted --src-ip 1.2.3.4

Needs root/admin (raw sockets), same as your sniffer.
"""

import argparse
import random
import time

from scapy.all import send, IP, TCP, ICMP, RandShort

SAFE_TARGETS = {"127.0.0.1", "localhost", "::1"}


def confirm_target(target, allow_any):
    if target in SAFE_TARGETS or allow_any:
        return
    print(f"[!] Refusing to send traffic to '{target}'.")
    print("    This script only targets localhost by default.")
    print("    If this is a machine YOU own/control on your own network,")
    print("    re-run with --i-own-this-target to proceed.")
    raise SystemExit(1)


def ping_flood(target, count=60, inter=0.01):
    print(f"[*] Ping flood: {count} ICMP packets -> {target}")
    send(IP(dst=target) / ICMP(), count=count, inter=inter, verbose=False)


def port_scan(target, num_ports=35, delay=0.05):
    print(f"[*] Port scan: probing {num_ports} distinct ports -> {target}")
    ports = random.sample(range(1, 65535), num_ports)
    for p in ports:
        send(IP(dst=target) / TCP(sport=RandShort(), dport=p, flags="S"), verbose=False)
        time.sleep(delay)


def syn_flood(target, count=110, dport=80, inter=0.01):
    print(f"[*] SYN flood: {count} bare SYN packets -> {target}:{dport}")
    send(
        IP(dst=target) / TCP(sport=RandShort(), dport=dport, flags="S"),
        count=count,
        inter=inter,
        verbose=False,
    )


def malformed_packets(target):
    print(f"[*] Malformed packets -> {target}")
    # TTL <= 0
    send(IP(dst=target, ttl=0) / TCP(sport=RandShort(), dport=80, flags="S"), verbose=False)
    # Contradictory flags: SYN+FIN and SYN+RST
    send(IP(dst=target) / TCP(sport=RandShort(), dport=80, flags="SF"), verbose=False)
    send(IP(dst=target) / TCP(sport=RandShort(), dport=80, flags="SR"), verbose=False)


def large_packet(target, size=1500):
    print(f"[*] Large packet (~{size} bytes) -> {target}")
    payload = b"A" * size
    send(IP(dst=target) / TCP(sport=RandShort(), dport=80) / payload, verbose=False)


def blacklisted_ip(target, src_ip):
    # Requires spoofing capability + that src_ip actually be in config.BLACKLISTED_IPS
    print(f"[*] Spoofed packet from blacklisted-looking source {src_ip} -> {target}")
    send(IP(src=src_ip, dst=target) / TCP(sport=RandShort(), dport=80, flags="S"), verbose=False)


def main():
    parser = argparse.ArgumentParser(description="IDS traffic generator (test/lab use only)")
    parser.add_argument("--target", default="127.0.0.1", help="Target IP (default: 127.0.0.1)")
    parser.add_argument(
        "--rule",
        choices=["ping_flood", "port_scan", "syn_flood", "malformed", "large_packet", "blacklisted", "all"],
        default="all",
    )
    parser.add_argument("--src-ip", default="1.2.3.4", help="Spoofed source IP for --rule blacklisted")
    parser.add_argument(
        "--i-own-this-target",
        action="store_true",
        help="Confirm you own/control the target (required for anything other than localhost)",
    )
    args = parser.parse_args()

    confirm_target(args.target, args.i_own_this_target)

    actions = {
        "ping_flood": lambda: ping_flood(args.target),
        "port_scan": lambda: port_scan(args.target),
        "syn_flood": lambda: syn_flood(args.target),
        "malformed": lambda: malformed_packets(args.target),
        "large_packet": lambda: large_packet(args.target),
        "blacklisted": lambda: blacklisted_ip(args.target, args.src_ip),
    }

    if args.rule == "all":
        for name, fn in actions.items():
            fn()
            time.sleep(1)
    else:
        actions[args.rule]()

    print("[*] Done. Check your IDS console/log output.")


if __name__ == "__main__":
    main()