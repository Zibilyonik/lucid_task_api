import jwt
import bcrypt
from datetime import datetime, timedelta

SECRET_KEY = "sludajf4ip32urt038uejfminposk-2398u-90-disnmi"
ALGORITHM = "HS256"

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

def create_token(user_id: int) -> str:
    payload = {"sub": user_id, "exp": datetime.now() + timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])["sub"]
    except:
        return None
