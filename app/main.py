from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from .database import engine
from passlib.context import CryptContext
from . import models
from .routers import post, user
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


"""------------------Routers for API functions-------------------------"""

app.include_router(post.router)
app.include_router(user.router)
