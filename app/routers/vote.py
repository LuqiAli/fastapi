from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, models, oauth2, schemas

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]    
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    
    post = db.query(models.post).filter(models.Post.id == vote.post_id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist.")
    
    voteQuery = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    foundVote = voteQuery.first()
    if vote.dir == 1:
        if foundVote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User: {current_user.id} has already voted on post {vote.post_id}")
        
        newVote = models.Vote(post_id = vote.post_id, user_id=current_user.id)
        db.add(newVote)
        db.commit()
        
        return {"message": "successfully added vote"}
        
    else:
        if not foundVote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote does not exist")
            
        voteQuery.delete(synchronize_session=False)
        db.commit()
    
        return {"message": "successfully deleted vote"}
        