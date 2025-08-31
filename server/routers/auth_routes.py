from database import users_collection, pwd_context
from fastapi import APIRouter, HTTPException
from models.user import User, UserCreate, UserRole

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register(user: UserCreate):
    if user.password != user.confirmed_password:
        raise HTTPException(status_code=400, detail="Passwords don't match")
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=409, detail="Username already exists")
    
    hashed_password = pwd_context.hash(user.password)
    
    new_user = User(
        username = user.username,
        email = user.email,
        password = hashed_password,
        role = UserRole.USER
    )
    
    await users_collection.insert_one(new_user.model_dump())
    
    return {"message": "User created successfully", 
            "user_data": {
                "username": user.username,
                "email": user.email,
                "role": UserRole.USER
            }}