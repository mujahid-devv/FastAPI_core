from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
def get_users():
    return [{"id": 1, "name": "Ali"}, {"id": 2, "name": "Sara"}]


@router.get("/{user_id}")
def get_user(user_id: int):
    return {"id": user_id, "name": "Ali"}


@router.post("/")
def create_user():
    return {"message": "User created"}


@router.delete("/{user_id}")
def delete_user(user_id: int):
    return {"message": f"User {user_id} deleted"}
