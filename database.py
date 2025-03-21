"""
Database configuration and session management.

This module provides SQLAlchemy engine setup, session factory,
and dependency injection for database access.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get database connection details from environment variables or use defaults
DB_USER = os.getenv("DB_USER", "fastapi_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fastapi_db")

DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_db():
    """
    Get a database session

    Yields:
        Session: Database session

    Notes:
        Use with FastAPI's Depends
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
