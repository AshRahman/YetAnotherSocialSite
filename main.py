from email.quoprimime import body_check
from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

@app.get("/") # This is a decorator, for API calls
async def root():
    return{"message": "Welcome to the API!!!"}


@app.get("/posts")
def get_posts():
    return {"data": "This is our post"}


@app.post("/createposts")
def create_posts(payLoad: dict = Body(...) ):
    print(payLoad)
    return {"new_post": f"title {payLoad['title']} content: {payLoad['content']}"}