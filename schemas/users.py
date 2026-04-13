from pydantic import BaseModel, Field, EmailStr


class UserCreate(BaseModel):
    name: str = Field(min_length=3, max_length=10)
    email: EmailStr
    age: int = Field(gt=0, lt=100)


class UserResponse(BaseModel):
    id: int
    name: str
