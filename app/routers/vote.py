from pyexpat import model
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schema, oauth2, models

router = APIRouter(
    prefix="/votes",
    tags=['Votes']
) 

@router.post("/", status_code= status.HTTP_201_CREATED)
def submit_vote(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    findPost = db.query(models.Posts).filter(models.Posts.id == vote.post_id)
    if not findPost.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No post with that id")
    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={"Error" : "You've already voted!"})
        new_vote = models.Votes(post_id = vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"Message" : "Success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error" : "Post not found"})
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"Message" : "Deleted Vote"}
        
    
