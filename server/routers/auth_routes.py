from fastapi import APIRouter, HTTPException, Depends, Response
from models.user import User, UserCreate, UserLogin, UserRole
from db.connection import client, get_users_collection, pwd_context
from datetime import datetime
from utils.logging import log
from utils.security import getAccessAndRefreshTokens
from models.user import UserPublic

router = APIRouter(prefix="", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate, users_collection=Depends(get_users_collection)):
    
    log(user, "info")
    
    if user.password != user.confirmed_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")

    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=409, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    
    now = datetime.now()

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role=UserRole.USER.value,
        created_at=now,
        updated_at=now
    )

    await users_collection.insert_one(new_user.model_dump())

    return {
        "message": "User created successfully",
        "user_data": new_user.model_dump(exclude={"password"}),
    }

@router.post("/login")
async def login(user: UserLogin, response: Response, users_collection=Depends(get_users_collection)):
    log(user, "info")
    
    existing_user = await users_collection.find_one({"username": user.username})
    if not existing_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    
    if not pwd_context.verify(user.password, existing_user["password"]):
        raise HTTPException(status_code=401, detail="Unauthorized access")
    
    tokens = getAccessAndRefreshTokens(existing_user)
    
    await users_collection.update_one(
        {"_id": existing_user["_id"]},
        {
            "$set": {
                "last_login": datetime.now(),
                "refresh_token": tokens[1]
            }
        },
        upsert=False
    )
    
    response.set_cookie(
        key="refresh_token",
        value=tokens[1],
        httponly=True,
        samesite="lax",
        max_age=24*60*60
    )
    
    response.set_cookie(
        key="access_token",
        value=tokens[0],
        httponly=True,
        samesite="lax",
        max_age=30*60
    )
    
    return {
        "message": "Login successful",
        "user_data": {
            "username": existing_user["username"],
            "email": existing_user["email"],
            "role": existing_user["role"],
        },
        "access_token": tokens[0],
        "refresh_token": tokens[1],
    }