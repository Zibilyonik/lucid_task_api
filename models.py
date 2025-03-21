"""
Database models for the application.

This module defines SQLAlchemy ORM models representing the
database tables and their relationships.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base


class User(Base):
    """
    User database model

    Attributes:
        id: Primary key
        email: User's email address
        password: Hashed password
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class Post(Base):
    """
    Post database model

    Attributes:
        id: Primary key
        text: Post content
        user_id: Foreign key to user
        created_at: Timestamp when post was created
    """

    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String(1000), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now)
