from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VoteBase(BaseModel):
    voted_party: str
    district: str
    constituency: str
    age_group: str
    caste: Optional[str] = None
    first_time_voter: bool = False
    pincode: Optional[str] = None
    device_fingerprint: str # Sent from frontend browser script

class VoteCreate(VoteBase):
    pass

class Vote(VoteBase):
    id: int
    ip_address: str
    created_at: datetime

    class Config:
        from_attributes = True
