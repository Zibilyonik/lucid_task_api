from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import User, Post
from schemas import UserCreate, UserLogin, PostCreate, PostResponse
from auth import hash_password, verify_password, create_token, decode_token
from cache import get_cached_posts, set_cached_posts

Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"token": create_token(new_user.id)}


@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"token": create_token(db_user.id)}


@app.post("/addpost")
def add_post(post: PostCreate, token: str, db: Session = Depends(get_db)):
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_post = Post(text=post.text, user_id=user_id)
    db.add(new_post)
    db.commit()
    return {"postID": new_post.id}


@app.get("/getposts")
def get_posts(token: str, db: Session = Depends(get_db)):
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    cached = get_cached_posts(user_id)
    if cached:
        return cached

    posts = db.query(Post).filter(Post.user_id == user_id).all()
    posts_data = [{"id": p.id, "text": p.text, "user_id": p.user_id} for p in posts]
    set_cached_posts(user_id, posts_data)
    return posts_data


@app.delete("/deletepost")
def delete_post(postID: int, token: str, db: Session = Depends(get_db)):
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    post = db.query(Post).filter(Post.id == postID, Post.user_id == user_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    db.delete(post)
    db.commit()
    return {"detail": "Post deleted"}
