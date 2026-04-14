from fastapi import APIRouter, Depends, Path, Query
from schemas.users import UserCreate, UserResponse
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

# NOTE: Route order matters — fixed paths before parameterized ones.
# Specific routes (e.g. /users/posts) must come before generic (e.g. /users/{user_id}).


def get_role():
    return "admin"


class CurrentUser:
    def __init__(self, role: str = Depends(get_role)):
        self.id = 1
        self.name = "Ali"
        self.role = role


def get_db():
    print("[DB] Connection opened")
    try:
        yield {"connected": True}
    finally:
        print("[DB] Connection closed")


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
def create_user(user: UserCreate, current_user: CurrentUser = Depends()):
    return {"message": "User created", "user": user, "current_user": current_user}


@router.get("/{user_id}/posts")
def get_posts(
    user_id: int = Path(..., ge=1),
    limit: int = Query(10, le=50),
    search: str | None = Query(None, min_length=3),
):
    return {"user_id": user_id, "limit": limit, "search": search}


@router.get("/{user_id}")
def get_user(user_id: int, db=Depends(get_db)):  # using db dependency
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
