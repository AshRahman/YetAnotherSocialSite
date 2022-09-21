from .. import models, schema
from fastapi import Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(prefix="/posts", tags=["Posts"])
"""----------------------Get All Post----------------------------"""


@router.get(
    "/", response_model=List[schema.Post]
)  # have to import List from typing lib, cause its a list of post
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return posts


"""----------------------Make new Post----------------------------"""


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
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


@router.get("/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return post


"""----------------------Get Id wise Post----------------------------"""


@router.get("/{id}", response_model=schema.Post)
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


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schema.Post)
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
