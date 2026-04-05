from sqlalchemy.orm import Session
import models, schemas

def check_duplicate_vote(db: Session, ip_address: str, device_fingerprint: str):
    """
    Check if a vote already exists for the given IP address and device fingerprint combination.
    """
    return db.query(models.Vote).filter(
        models.Vote.ip_address == ip_address,
        models.Vote.device_fingerprint == device_fingerprint
    ).first()

def create_vote(db: Session, vote: schemas.VoteCreate, ip_address: str):
    """
    Create a new vote in the database.
    """
    db_vote = models.Vote(
        **vote.model_dump(),
        ip_address=ip_address
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return db_vote

def get_votes(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all votes (Admin use mostly).
    """
    return db.query(models.Vote).offset(skip).limit(limit).all()

def delete_vote(db: Session, vote_id: int):
    """
    Delete a vote by ID.
    """
    db_vote = db.query(models.Vote).filter(models.Vote.id == vote_id).first()
    if db_vote:
        db.delete(db_vote)
        db.commit()
    return db_vote
