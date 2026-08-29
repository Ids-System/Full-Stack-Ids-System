from dataclasses import dataclass
from typing import Optional

@dataclass
class CapturedPacket:
    Source_IP : str
    Destination_IP : str
    Source_Port : Optional[int]
    Destination_Port : Optional[int]    
    Protocol : str
    Packet_Size : int 
    TTL : Optional[int]
    TCP_Flags : Optional[str]
    Time_Stamps : float

@dataclass
class Attack:
    attack : str
    severity : str
    source_ip : str
    destination_ip : str
    protocol : str
    port : int
    timestamp : str
    description : str
