"""
Post-related business logic.

This module provides service functions for post operations,
including creating, retrieving, and deleting posts.
"""

from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import Post
from schemas import PostCreate
from cache import get_cached_posts, set_cached_posts


def create_post(db: Session, user_id: int, post_data: PostCreate):
    """
    Create a new post for a user

    Args:
        db: Database session
        user_id: ID of the user creating the post
        post_data: Post creation data with validated text

    Returns:
        Post: Created post object
    """
    new_post = Post(text=post_data.text, user_id=user_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def get_user_posts(db: Session, user_id: int):
    """
    Get all posts for a user with caching

    Args:
        db: Database session
        user_id: ID of the user

    Returns:
        list: List of user's posts
    """
    # Check cache first
    cached = get_cached_posts(user_id)
    if cached:
        return cached

    # Get from database if not in cache
    posts = db.query(Post).filter(Post.user_id == user_id).all()
    posts_data = [
        {"id": p.id, "text": p.text, "user_id": p.user_id, "created_at": p.created_at}
        for p in posts
    ]

    # Update cache for future requests
    set_cached_posts(user_id, posts_data)
    return posts_data


def delete_post(db: Session, post_id: int, user_id: int):
    """
    Delete a user's post

    Args:
        db: Database session
        post_id: ID of the post to delete
        user_id: ID of the post owner

    Returns:
        bool: True if deleted successfully

    Raises:
        HTTPException: If post not found or doesn't belong to user
    """
    post = db.query(Post).filter(Post.id == post_id, Post.user_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return True
