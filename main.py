
from hashlib import new
from turtle import pos
from typing import Optional
from fastapi import FastAPI,Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#schema model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True 
    rating: Optional[int]=None

my_posts=[{"title": "title of post 1", "content": "content of post 1", "id": 1},
          {"title": "favourite food", "content": "pizza","id":2 }]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
@app.get("/") # This is a decorator, for API calls
async def root():
    return{"message": "Welcome to the API!!!"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}

#
@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    
   
    post_dict= post.dict() #makes the post into python dictionary
    post_dict['id'] = randrange(0,1000000) #assigns random number into id
    my_posts.append(post_dict) #appends the post into dictionary
    return {"data":post_dict}
#title str, content str, category, bool published 
@app.get("/posts/latest")
def get_latest_post():
    post=my_posts[len(my_posts)-1]
    return{"detail":post}

@app.get("/posts/{id}")
def get_post(id:int, response: Response):
    post=find_post(id) #the id comes as a string so we need to convert
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail= f"post with id: {id} was not found")
        '''response.status_code = status.HTTP_404_NOT_FOUND #uses the status library
        return{"message": f"post with id: {id} was not found"}  
        '''  
    return {"post_detail": post}
    
