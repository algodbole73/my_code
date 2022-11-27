from typing import List, Optional

from fastapi import (APIRouter, Depends, FastAPI, HTTPException, Response,
                     status)
from sqlalchemy.orm import Session
from sqlalchemy import  func

from .. import autho02, models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


#New nosql code 
@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts =db.query(models.Post).all()
    #post_select =db.query(models.Post)
    #print(post_select)
    return{"data":posts}

#get all posts from database 
#@router.get("/", response_model=List[schemas.Postres])
@router.get("/",response_model=List[schemas.Postout])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(autho02.get_current_user),
        limit:int = 10 ,skip:int = 0, search: Optional[str] = ""):
    print(current_user.id)
    #getposts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    getposts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
   
    #print(getposts)   
    return getposts
    
#find post by id from database 
@router.get("/{id}")
def get_post(id:int, db: Session = Depends(get_db), current_user:int = Depends(autho02.get_current_user)):
    #cursor.execute("""select * from post where id = %s """ , (str (id)))
    #getpost = cursor.fetchone()
    #print(getpost)
    getpostid = db.query(models.Post).filter(models.Post.id == id).first()
    getpost = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
   
    print(getpostid)
    if not getpostid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message":f"post with id: {id} not found"}
    if getpostid.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    return getpost


#Create a new post
@router.post("/", status_code=status.HTTP_201_CREATED,response_model= schemas.Postres)
def creat_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int = Depends(autho02.get_current_user)):
    #cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING * """ , (post.title,post.content,post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    #new_post = models.Post(title=post.title,content=post.content, published = post.published)
    print(current_user.id)
    #new_post = models.Post(**post.dict())
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#Deleteing post
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int, db: Session = Depends(get_db), current_user:int = Depends(autho02.get_current_user)): 
    #cursor.execute("""DELETE from post where id = %s returning * """ , (str (id),))
    #delpost = cursor.fetchone()   
    #conn.commit() 
    delpost= db.query(models.Post).filter(models.Post.id == id) 
    post = delpost.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    delpost.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    
#update post
 
@router.put("/{id}", response_model=schemas.Postres)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(autho02.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()