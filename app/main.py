from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from .database import Sessionlocal, engine
from . import models
import psycopg2
import time
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


"""----------------------Post Schema Model----------------------------"""


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


"""----------------------Database Connection----------------------------"""
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="YASS",
            user="postgres",
            password="123",
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("connection successful")
        break
    except Exception as error:
        print("Connection failed")
        print("Error: ", error)
        time.sleep(2)

"""----------------------Custom Functions----------------------------"""


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):  # enumerate adds counter
        if p["id"] == id:
            return i


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status": "Success"}


"""----------------------Root Page----------------------------"""


@app.get("/")  # This is a decorator, for API calls
async def root():
    return {"message": "Welcome to the API!!!"}


"""----------------------Get All Post----------------------------"""


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


"""----------------------Make new Post----------------------------"""


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute(
        """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING* """,
        (post.title, post.content, post.published),
    )  # this is sql injection safe
    conn.commit()  # for inserting data you have to commit
    new_post = cursor.fetchone()

    return {"data": new_post}


# title str, content str, category, bool published


"""----------------------Get Latest Post----------------------------"""


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"detail": post}


"""----------------------Get Id wise Post----------------------------"""


@app.get("/posts/{id}")
def get_post(id: str):
    cursor.execute("""SELECT * FROM posts where id= %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )

    return {"post_detail": post}


"""----------------------Delete Post----------------------------"""


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""----------------------Update Post----------------------------"""


@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    updated_post = cursor.execute(
        """UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *""",
        (post.title, post.content, post.published, str(id)),
    )
    conn.commit()
    if updated_post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    return {"data": updated_post}
