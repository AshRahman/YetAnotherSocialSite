from fastapi import FastAPI, Response, status, HTTPException, Depends
from psycopg2.extras import RealDictCursor
from .database import engine, get_db
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schema, utils
import psycopg2
import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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


"""----------------------Root Page----------------------------"""


@app.get("/")  # This is a decorator, for API calls
async def root():
    return {"message": "Welcome to the API!!!"}


"""----------------------Get All Post----------------------------"""


@app.get(
    "/posts", response_model=List[schema.Post]
)  # have to import List from typing lib, cause its a list of post
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return posts


"""----------------------Make new Post----------------------------"""


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING* """,
    #     (post.title, post.content, post.published),
    # )  # this is sql injection safe
    # conn.commit()  # for inserting data you have to commit
    # new_post = cursor.fetchone()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


# title str, content str, category, bool published


"""----------------------Get Latest Post----------------------------"""


@app.get("/posts/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post


"""----------------------Get Id wise Post----------------------------"""


@app.get("/posts/{id}", response_model=schema.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute("""SELECT * FROM posts where id= %s """, (str(id)))
    # post = cursor.fetchone()
    post = (
        db.query(models.Post).filter(models.Post.id == id).first()
    )  # doesn't work if first is not given,recursive error

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} was not found",
        )
    return post


"""----------------------Delete Post----------------------------"""


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # deleting post

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


"""----------------------Update Post----------------------------"""


@app.put("/posts/{id}", response_model=schema.Post)
def update_post(
    id: int, updated_post: schema.PostCreate, db: Session = Depends(get_db)
):

    # updated_post = cursor.execute(
    #     """UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, str(id)),
    # )
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )
    post_query.update(
        updated_post.dict(),
        synchronize_session=False,
    )
    db.commit()
    return post_query.first()


"""---------------USER---------------------------------------"""


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash the password- user.password
    hashed_pass = utils.hash(user.password)
    user.password = hashed_pass
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id:{id} does not exist",
        )
    return user
