from dotenv import load_dotenv, find_dotenv
from datetime import datetime, timedelta, timezone
import os
from jose import jwt
from models.user import User

load_dotenv(find_dotenv())

def create_access_token(data: dict, expires_in_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15))):
    to_encode = data.copy()
    if "id" in to_encode and not isinstance(to_encode["id"], str):
        to_encode["id"] = str(to_encode["id"])

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_in_minutes)
    to_encode.update({"exp": expire, "iat": now})
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

    
def create_refresh_token(user_id: str, expires_in_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", 10080))):
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=expires_in_minutes)
    to_encode = {"id": str(user_id), "exp": expire, "iat": now}
    return jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))

def verify_token(token: str):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
    
def getAccessAndRefreshTokens(user: User | dict):
    if isinstance(user, dict):
        user = User(**user)    

    user_data = user.to_dict()

    access_token = create_access_token(data=user_data)
    refresh_token = create_refresh_token(user_id=user_data["id"])
    return access_token, refresh_token
