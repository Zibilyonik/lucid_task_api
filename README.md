# Lucid Task API

A FastAPI-based RESTful API for user authentication and post management, following the MVC design pattern.

## Overview

This project implements a secure API with token-based authentication, allowing users to create accounts, log in, and manage text posts. It features request validation, caching, and follows best practices for API design.

## Features

- **User Authentication**: Secure signup and login with JWT tokens
- **Post Management**: Create, retrieve and delete text posts
- **Request Validation**: Size limitations and field validation
- **Response Caching**: 5-minute caching for repeated requests
- **MVC Architecture**: Clean separation of models, views, and controllers
- **Security**: Password hashing, token-based authentication

## Technologies Used

- **Python**: Core language
- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database operations
- **Pydantic**: Data validation and settings management
- **JWT**: Token-based authentication
- **bcrypt**: Password hashing
- **MySQL**: Database (via SQLAlchemy)

## Project Structure

```
lucid_task_api/
├── main.py              # FastAPI application and routes
├── models.py            # SQLAlchemy database models
├── schemas.py           # Pydantic validation schemas
├── database.py          # Database connection setup
├── auth.py              # Authentication utilities
├── user_service.py      # User-related business logic
├── post_service.py      # Post-related business logic
├── cache.py             # In-memory caching implementation
├── middleware.py        # Custom middleware components
└── .gitignore           # Git ignore file
```

## API Documentation

### Authentication Endpoints

#### `POST /signup`
Register a new user.
- **Request Body**: `{ "email": "user@example.com", "password": "securepassword" }`
- **Response**: `{ "token": "jwt_token_string" }`

#### `POST /login`
Authenticate an existing user.
- **Request Body**: `{ "email": "user@example.com", "password": "securepassword" }`
- **Response**: `{ "token": "jwt_token_string" }`
- **Error Response**: `{ "detail": "Invalid credentials" }`

### Post Management Endpoints

#### `POST /addpost`
Create a new post (requires authentication).
- **Request Body**: `{ "text": "Post content here" }`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "postID": 1 }`
- **Error Response**: `{ "detail": "Invalid token" }`

#### `GET /getposts`
Retrieve all posts for the authenticated user.
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `[{ "id": 1, "text": "Post content", "user_id": 1, "created_at": "2023-01-01T12:00:00" }]`
- **Notes**: Responses are cached for 5 minutes per user

#### `DELETE /deletepost`
Delete a post by ID.
- **Query Parameters**: `post_id=1`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{ "detail": "Post deleted" }`
- **Error Response**: `{ "detail": "Post not found" }`

## Setup and Installation

1. **Clone the repository**:
   ```
   git clone https://github.com/yourusername/lucid_task_api.git
   cd lucid_task_api
   ```

2. **Create a virtual environment**:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```
   uvicorn main:app --reload
   ```

5. **Access the API documentation**:
   Open your browser and navigate to `http://localhost:8000/docs`

## Usage Examples

### Create a new user

```bash
curl -X POST http://localhost:8000/signup \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Login

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'
```

### Create a post

```bash
curl -X POST http://localhost:8000/addpost \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"text": "This is my first post!"}'
```

### Get user's posts

```bash
curl -X GET http://localhost:8000/getposts \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Delete a post

```bash
curl -X DELETE "http://localhost:8000/deletepost?post_id=1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Security Considerations

- JWT secret key is sent separately via email
- Password hashing is implemented using bcrypt
- Request size is limited to prevent abuse

---

This project was developed as a coding task following the MVC design pattern with FastAPI.
