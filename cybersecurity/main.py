import os
import sys
import config
from sniffer import start_sniffing

def ensure_logs_dir():
    os.makedirs("logs", exist_ok=True)

def main():
    ensure_logs_dir()
    interface = sys.argv[1] if len(sys.argv) > 1 else None

    print("=" * 55)
    print("IDS Rule-Based Engine")
    print(f"Sending alerts to: {config.API_URL}")
    print(f" Interface: {interface or '(default)'}")
    print("=" * 55)

    try:
        start_sniffing(interface=interface)
    except PermissionError:
        print("[Error] Packet sniffing needs elevated privileges")
        print("Try: sudo python3 main.py")
    except KeyboardInterrupt:
        print("\n[IDS] Stopped by user.")

if __name__ == "__main__": 
    main()