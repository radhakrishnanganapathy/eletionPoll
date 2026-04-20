from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, index=True, nullable=False)
    device_fingerprint = Column(String, index=True, nullable=False)
    voted_party = Column(String, nullable=False)
    district = Column(String, nullable=False)
    constituency = Column(String, nullable=False)
    age_group = Column(String, nullable=False)
    caste = Column(String, nullable=True) # Optional
    first_time_voter = Column(Boolean, default=False)
    is_pondicherry = Column(Boolean, default=False)
    pincode = Column(String, nullable=True) # Optional
    created_at = Column(DateTime(timezone=True), server_default=func.now())
