from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from fastapi import openapi
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Post(BaseModel):
    title:str
    content:str
    published:bool = True
    #rating: Optional[int]  = None

#Connect to database
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='sysadmin', cursor_factory= RealDictCursor)
        cursor = conn.cursor()
        print ("database connection is successfull")
        break
    except Exception as error:
        print(f"database connection failed {error}")
        time.sleep(10)


my_posts = [{"title":"food","content":"pizza","id":1},
             {"title":"place","content":"paris","id":2} ]

@app.get("/")
def get_user():
    return {"message": "Get fast api call"}

#get all posts from database 
@app.get("/posts")
def get_posts():
    cursor.execute("""select * from post""")
    posts = cursor.fetchall()
    print(posts)
    return{"data": posts}

#Create a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def creat_posts(post:Post):
    cursor.execute("""INSERT INTO post (title,content,published) VALUES (%s,%s,%s) RETURNING * """ , (post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{"data":new_post}

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

#find post by id from database 
@app.get("/posts/{id}")
def get_post(id:int, response:Response):
    cursor.execute("""select * from post where id = %s """ , (str (id)))
    getpost = cursor.fetchone()
    print(getpost)
    
    if not getpost:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return{"message":f"post with id: {id} not found"}
     
    return{"post details" : getpost }

#Deleteing post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def del_post(id: int): 
    cursor.execute("""DELETE from post where id = %s returning * """ , (str (id),))
    delpost = cursor.fetchone()   
    conn.commit() 
    if delpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update post
@app.put("/posts/{id}")
def update_post(id: int, post: Post): 
    cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s where id = %s returning * """ , (post.title,post.content,post.published,str (id)))
    conn.commit() 
    updaetdpost = cursor.fetchone()    
    if updaetdpost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found")
    return{"data": updaetdpost}