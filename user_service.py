"""
User-related business logic.

This module provides service functions for user operations,
including user creation, authentication, and profile management.
"""

from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from models import User
from schemas import UserCreate
from auth import hash_password, verify_password, decode_token
from database import get_db


def create_user(db: Session, user_data: UserCreate):
    """
    Create a new user in the database

    Args:
        db: Database session
        user_data: User creation data with validated email and password

    Returns:
        User: Created user object

    Raises:
        HTTPException: If email already exists
    """
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)
    new_user = User(email=user_data.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user with email and password

    Args:
        db: Database session
        email: User email
        password: Plain text password

    Returns:
        User: Authenticated user object or None if authentication fails
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user


def get_current_user(token: str, db: Session = Depends(get_db)):
    """
    Validate token and return current user

    Args:
        token: JWT authentication token
        db: Database session

    Returns:
        User: Current authenticated user

    Raises:
        HTTPException: If token is invalid or user not found
    """
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
