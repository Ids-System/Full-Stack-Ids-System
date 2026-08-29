import time 
import detector
from models import CapturedPacket
from scapy.all import sniff, IP, TCP, UDP, ICMP, ARP

def extract_packet_info(pkt):

    try:
        if pkt.haslayer(IP):
            ip_layer = pkt[IP]

            source_port = None
            destination_port = None
            tcp_flags = None
            protocol = "Other"

            if pkt.haslayer(TCP):
                protocol = "TCP"
                source_port = pkt[TCP].sport
                destination_port = pkt[TCP].dport
                tcp_flags = str(pkt[TCP].flags)

            elif pkt.haslayer(UDP):
                protocol = "UDP"
                source_port = pkt[UDP].sport
                destination_port = pkt[UDP].dport

            elif pkt.haslayer(ICMP):
                protocol = "ICMP"

            return CapturedPacket(
                Source_IP = ip_layer.src,
                Destination_IP = ip_layer.dst,
                Source_Port = source_port,
                Destination_Port = destination_port,
                Protocol = protocol,
                Packet_Size = len(pkt),
                TTL = ip_layer.ttl,
                TCP_Flags = tcp_flags,
                Time_Stamps = time.time()

            )

        elif pkt.haslayer(ARP):
            return CapturedPacket(
                Source_IP = pkt[ARP].psrc,
                Destination_IP = pkt[ARP].pdst,
                Source_Port = None,
                Destination_Port = None,
                Protocol = "ARP",
                Packet_Size = len(pkt),
                TTL = None,
                TCP_Flags = None,
                Time_Stamps = time.time()
            )


    except Exception as e:
        print(f"[Sniffer] Error parsing paket: {e}")
    return None

def packet_callback(pkt):

    captured = extract_packet_info(pkt)
    if captured:
        detector.process_packet(captured)
    
def start_sniffing(interface=None):

    print(f"[Sniffer] Starting packet capture... (Ctrl+C to Stop)") 
    sniff(iface = interface, prn=packet_callback, store = False)