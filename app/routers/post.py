from unittest import result
from fastapi import Response, HTTPException, Depends, APIRouter, status
from typing import List, Optional
from app import oauth2
from .. import models, schema
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
) 

@router.get("/", response_model=List[schema.PostResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    print(limit)
    posts = db.query(models.Posts).filter(models.Posts.title.contains(search)).limit(limit=limit).offset(skip).all()
    return posts

@router.get("/likes", response_model=List[schema.NoOfLikes])
def get_post_with_likes(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    results = db.query(models.Posts, func.count(models.Votes.post_id).label("no_of_likes")).join(models.Votes, models.Votes.post_id == models.Posts.id, isouter=True).group_by(models.Posts.id)
    print(results)
    return results.all()


@router.get("/owner_id:{owner_id}")
def get_only_user_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    ownerPosts = db.query(models.Posts).filter(models.Posts.owner_id == current_user.id).all()
    return ownerPosts

@router.get("/id:{id}", response_model=schema.PostResponse)
def get_one_post(id: int, response: Response, db : Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    print(post)
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # gotPost = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error" : "No Post found"})
    return post


@router.delete("/id:{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    postQuery = db.query(models.Posts).filter(models.Posts.id == id)
    if not postQuery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error" : "No Post To Delete"})
    if postQuery.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"Error" : "Not authorized"})
    postQuery.delete(synchronize_session=False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.post("/", response_model=schema.PostResponse)
def create_post(post: schema.PostBase, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(current_user.id)
    new_post = models.Posts(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    response.status_code = status.HTTP_201_CREATED
    return new_post

@router.put("/id:{id}", response_model=schema.PostResponse)
def put_post(id:int, post:schema.PostBase, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))
    # print(post)
    # updatedPost = cursor.fetchone()
    # conn.commit()
    postQuery = db.query(models.Posts).filter(models.Posts.id == id)
    if not postQuery.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error" : "No Post To Update"})
    if postQuery.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={"Error" : "Not authorized"})
    postQuery.update(post.dict(), synchronize_session=False)
    db.commit()
    return postQuery.first()

