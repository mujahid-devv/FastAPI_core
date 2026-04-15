from fastapi import APIRouter, Depends, Path, Query, BackgroundTasks
from schemas.users import UserCreate, UserResponse
from typing import List
from pydantic import EmailStr

router = APIRouter(prefix="/users", tags=["Users"])

# NOTE: Route order matters — fixed paths before parameterized ones.
# Specific routes (e.g. /users/posts) must come before generic (e.g. /users/{user_id}).
# If you have dependencies with yield, the exit code will run after the middleware.
# If there were any background tasks, they will run after all the middleware.
# execution order is: Middleware → Path Operation → Dependencies (yield cleanup) → Background Tasks


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


# Simple BackgroundTasks: use when task is specific to this endpoint only
# BackgroundTasks in dependency: use when task is reusable across multiple endpoints
def write_notification(email: str, message: str = ""):
    with open("log.txt", mode="a") as email_file:
        content = f"notification for {email} : {message} \n"
        email_file.write(content)


def get_notification_message():
    return "simple background task"


# background Task route
@router.post("/send-notification/{email}")
async def send_notification(
    email: EmailStr,
    background_tasks: BackgroundTasks,
    message: str = Depends(get_notification_message),
):
    background_tasks.add_task(write_notification, email, message=message)
    return {"message": "notification sent in the background"}


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
