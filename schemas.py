"""
Pydantic schemas for request and response validation.

This module defines Pydantic models used for validating
incoming requests and formatting outgoing responses.
"""

from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, EmailStr, constr, field_validator


class UserCreate(BaseModel):
    """
    Schema for creating users

    Attributes:
        email: Valid email address
        password: Password with minimum length of 6 characters
    """

    email: EmailStr
    password: Annotated[str, constr(min_length=6)]

    @field_validator("email")
    def email_must_be_valid(self, v):
        """
        Validate email format

        Args:
            v: Email value to validate

        Returns:
            str: Validated email

        Raises:
            ValueError: If email format is invalid
        """
        # Additional email validation
        if not v or "@" not in v:
            raise ValueError("Invalid email format")
        # Check domain part
        domain = v.split("@")[1] if "@" in v else ""
        if not domain or "." not in domain:
            raise ValueError("Invalid email domain")
        return v


class UserLogin(BaseModel):
    """
    Schema for user login

    Attributes:
        email: User's email address
        password: User's password
    """

    email: EmailStr
    password: str


class PostCreate(BaseModel):
    """
    Schema for creating posts

    Attributes:
        text: Post content, 1MB max size
    """

    text: Annotated[str, constr(min_length=1, max_length=1000000)]  # 1MB limit

    @field_validator("text")
    def text_not_too_long(self, v):
        """
        Validate post text is within size limits

        Args:
            v: Post text to validate

        Returns:
            str: Validated post text

        Raises:
            ValueError: If text exceeds size limit
        """
        # Additional size validation
        if len(v.encode("utf-8")) > 1_000_000:  # 1MB in bytes
            raise ValueError("Post content exceeds 1MB limit")
        return v


class PostResponse(BaseModel):
    """
    Schema for post responses

    Attributes:
        id: Post ID
        text: Post content
        user_id: Owner's user ID
        created_at: Post creation timestamp
    """

    id: int
    text: str
    user_id: int
    created_at: Optional[datetime] = None

    class Config:
        """
        Pydantic model configuration

        This enables ORM mode for converting SQLAlchemy models
        to Pydantic models automatically, maintaining relationships.
        """

        from_attributes = True
