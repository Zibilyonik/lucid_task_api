"""
Main application entry point for the API.

This module initializes the FastAPI application, sets up routes,
and connects all the components together.
"""

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import User
from schemas import UserCreate, UserLogin, PostCreate
from auth import create_token
from user_service import create_user, authenticate_user, get_current_user
from post_service import create_post, get_user_posts, delete_post
from middleware import RequestSizeLimiter

# Create database tables
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(RequestSizeLimiter, max_request_size=1000)


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user

    Args:
        user: User registration data
        db: Database session

    Returns:
        dict: Authentication token
    """
    new_user = create_user(db, user)
    return {"token": create_token(new_user.id)}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a token

    Args:
        user: User login credentials
        db: Database session

    Returns:
        dict: Authentication token

    Raises:
        HTTPException: If credentials are invalid
    """
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": create_token(authenticated_user.id)}


@app.post("/addpost")
def add_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Create a new post

    Args:
        post: Post creation data
        current_user: Authenticated user
        db: Database session

    Returns:
        dict: Created post ID
    """
    new_post = create_post(db, current_user.id, post)
    return {"postID": new_post.id}


@app.get("/getposts")
def get_posts(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    Get all posts for the authenticated user

    Args:
        current_user: Authenticated user
        db: Database session

    Returns:
        list: User's posts
    """
    return get_user_posts(db, current_user.id)


@app.delete("/deletepost")
def delete_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Delete a post

    Args:
        post_id: ID of the post to delete
        current_user: Authenticated user
        db: Database session

    Returns:
        dict: Success message
    """
    delete_post(db, post_id, current_user.id)
    return {"detail": "Post deleted"}
