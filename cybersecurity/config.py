#FastAPI Backend API URL
API_URL = "http://127.0.0.1:8000/engine/report"
API_TIMEOUT = 3

#RULE 1: Ping Flood - 50 ICMP packets within 1 seconds
PING_FLOOD_COUNT = 50
PING_FLOOD_WINDOW = 1

#RULE 2: Port Scan - 30 ports within 10 seconds
PORT_SCAN_COUNT = 30
PORT_SCAN_WINDOW = 10

#RULE 3: SYN Flood - SYN packets without ACK
SYN_FLOOD_COUNT = 100
SYN_FLOOD_WINDOW = 5

#RULE 4: Blacklisted IP'S
BLACKLISTED_IPS = {
    "1.2.3.4",
    "5.6.7.8",
    #add blacklisted or bad ips
}

#RULE 5: Malformed Packet
#Invalid TCP Header -> Alert

#RULE 6: Large Packet Size
LARGE_PACKET_THRESHOLD = 8928 #for localhost

#LOGS
LOG_FILE = "logs/ids_engine.log"
