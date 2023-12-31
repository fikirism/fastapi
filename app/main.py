from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI(
    title="FASTAPI CRUD OPERATION APP",
    docs_url="/",
    description="learning fastapi"
)

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts =[{"title": "title one", "content": "content one", "id": 1},{"title": "title two", "content": "content two","id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/')
def root():
    return {"message":"fikiri"}

@app.get("/post")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(payload: Post):
    post_dict = payload.model_dump()
    post_dict["id"] = randrange(0, 10)
    my_posts.append(post_dict)
    return{"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    latest = my_posts[len(my_posts)-1]
    return {"detail": latest}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index),
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int,payload: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    post_dict = payload.model_dump()
    post_dict['id']=id
    my_posts[index]=post_dict
    return{'data': post_dict}