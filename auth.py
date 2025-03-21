"""
Authentication utilities and JWT token management.

This module handles password hashing, JWT token creation,
verification, and token-based authentication.
"""

import logging
import os
from datetime import datetime, timedelta
import jwt
import bcrypt

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    logging.warning("JWT_SECRET_KEY not found in .env. Using default key (NOT SECURE)")
    SECRET_KEY = "FnbXbrysHdvgoP3to8JoAPZf7/SFWdEcG6lSXZbAHF4="

ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a password against its hash

    Args:
        password: Plain text password
        hashed: Hashed password

    Returns:
        bool: True if password matches hash
    """
    return bcrypt.checkpw(password.encode(), hashed.encode())


def create_token(user_id: int) -> str:
    """
    Create a JWT token for a user

    Args:
        user_id: User ID to encode in token

    Returns:
        str: JWT token
    """
    payload = {"sub": user_id, "exp": datetime.now() + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str):
    """
    Decode a JWT token

    Args:
        token: JWT token

    Returns:
        int: User ID from token or None if invalid
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    except jwt.ExpiredSignatureError:
        logging.error("Token expired")
        return None
    except jwt.InvalidTokenError:
        logging.error("Invalid token")
        return None
    except (TypeError, ValueError) as e:
        logging.error("Error in token format: %s", e)
        return None
