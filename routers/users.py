from fastapi import APIRouter, Query, Path
from schemas.users import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# NOTE: Route order matters — fixed paths before parameterized ones.
# Specific routes (e.g. /users/posts) must come before generic (e.g. /users/{user_id}).


@router.get("/", response_model=List[UserResponse])
def get_users():
    return [
        {
            "id": 1,
            "name": "Ali",
            "role": "admin",
            "hobbies": ["reading", "cricket"],
            "address": {"city": "Karachi", "country": "Pakistan"},
        },
        {
            "id": 2,
            "name": "Sara",
            "role": "user",
            "hobbies": ["painting"],
            "address": {"city": "Lahore", "country": "Pakistan"},
        },
    ]


@router.post("/")
def create_user(user: UserCreate):
    return {"message": "User created", "user": user}


@router.get("/{user_id}/posts")
def get_posts(
    user_id: int = Path(..., ge=1),
    limit: int = Query(10, le=50),
    search: str | None = Query(None, min_length=3),
):
    return {"user_id": user_id, "limit": limit, "search": search}


@router.get("/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": "Ali",
        "role": "admin",
        "hobbies": ["reading", "cricket"],
        "address": {"city": "Karachi", "country": "Pakistan"},
    }


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}
