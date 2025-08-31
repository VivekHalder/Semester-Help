from datetime import datetime
from pydantic import BaseModel, EmailStr, Enum, Field, model_validator
from typing import Optional
from typing_extensions import Self

class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    
class User(BaseModel):
    id: Optional[str] = None
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.USER
    mobile: Optional[str] = None
    location: Optional[str] = None
    github: Optional[str] = None
    linkedin: Optional[str] = None
    portfolio: Optional[str] = None 
    
class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=8)
    confirmed_password: str = Field(min_length=8)
    
    @model_validator(mode='after')
    def check_confirmed_password(self) -> Self:
        if self.password != self.confirmed_password:
            raise ValueError("Passwords do not match")
        return self
    
class UserPublic(BaseModel):
    username: str
    email: EmailStr
    role: UserRole
    mobile: str | None = None
    location: str | None = None
    github: str | None = None
    linkedin: str | None = None
    portfolio: str | None = None
    created_at: datetime | None = None

class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic
