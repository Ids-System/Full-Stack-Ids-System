from pydantic import BaseModel
from pydantic.networks import IPvAnyAddress
from datetime import datetime

class Report(BaseModel):
    attack: str
    severity: str
    source_ip: IPvAnyAddress
    destination_ip: IPvAnyAddress
    protocol: str
    port: int
    timestamp: datetime
    description: str
    