from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PostCreate(BaseModel):
    text: constr(min_length=1, max_length=1000000)  # 1MB limit

class PostResponse(BaseModel):
    id: int
    text: str
    user_id: int
