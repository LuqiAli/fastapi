from typing import List, Optional
from .. import models, schemas, oauth2
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..database import get_db

router = APIRouter(
    prefix="/posts",  
    tags=["Posts"]
)



@router.get("/", response_model=List[schemas.PostOut])
def getPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall() 
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return post

@router.get("/own", response_model=List[schemas.PostOut])
def getOwnPosts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
     
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall() 
    
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(
        models.Post.title.contains(search), models.Post.owner_id == current_user.id).limit(limit).offset(skip).all()
        
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def createPosts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    
    # newPost = cursor.fetchone()
    # conn.commit()
    
    
    newPost = models.Post(owner_id=current_user.id, **post.dict())
    
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    
    return newPost


@router.get("/{id}", response_model=schemas.PostOut)
def getPost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found.")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deletedPost = cursor.fetchone()
    # conn.commit()
    
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    
    post = postQuery.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    
    postQuery.delete(synchronize_session=False)
    db.commit()
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

 
@router.put("/{id}", response_model=schemas.Post)
def updatePost(id: int, updatedPost: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.getCurrentUser)):
    
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, id))
    # updatedPost = cursor.fetchone()
    # conn.commit()
    
    postQuery = db.query(models.Post).filter(models.Post.id == id)
    post = postQuery.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
        
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
        
    postQuery.update(updatedPost.dict(), synchronize_session=False)
    db.commit()

    return postQuery.first()