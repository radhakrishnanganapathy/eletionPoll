from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, get_db
import logging

# Ensure tables are created on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Election Poll API")

# Allow requests from the frontend (Adjust to restrict origins in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/vote", response_model=schemas.Vote)
def cast_vote(vote: schemas.VoteCreate, request: Request, db: Session = Depends(get_db)):
    # 1. Get Client IP Address
    # In cloud environments (like Render), 'x-forwarded-for' header contains actual IP
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host

    # 2. Check for duplicate vote
    existing_vote = crud.check_duplicate_vote(db, ip_address=client_ip, device_fingerprint=vote.device_fingerprint)
    if existing_vote:
        raise HTTPException(status_code=400, detail="You already caste your vote.")

    # 3. Insert and return the successful vote
    try:
        new_vote = crud.create_vote(db, vote=vote, ip_address=client_ip)
        return new_vote
    except Exception as e:
        logging.error(f"Error casting vote: {e}")
        raise HTTPException(status_code=500, detail="An error occurred saving your vote.")

@app.get("/api/votes", response_model=list[schemas.Vote])
def read_votes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Basic route to verify votes are being saved. You may want to restrict access to this!
    """
    votes = crud.get_votes(db, skip=skip, limit=limit)
    return votes

@app.delete("/api/votes/{vote_id}")
def delete_vote_by_id(vote_id: int, db: Session = Depends(get_db)):
    """
    Delete a vote by its ID.
    """
    deleted_vote = crud.delete_vote(db, vote_id=vote_id)
    if not deleted_vote:
        raise HTTPException(status_code=404, detail="Vote not found.")
    return {"message": "Vote successfully deleted.", "deleted_id": vote_id}

@app.get("/")
def read_root():
    return {"message": "Welcome to the Election Poll API"}
