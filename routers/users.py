# Query and Path params
# route order matters significantly
# fixed routes should always come before parameterized routes
# More specific routes must come before less specific ones.
# |-> the route with less params should come earlier then the route with more params
# 5. Router Inclusion Order (APIRouter)
# query params are not affected by the order as they do not compete with the route resolution
# When using include_router(), the order of inclusion follows the same rules
from fastapi import APIRouter
from fastapi import Query, Path

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


@router.get("/products/{category}")
def get_products(
    category: str,
    max_price: int,
    min_price: int,
    in_stock: bool = True,
    order_by: str = "price",
    limit: int = 10,
):
    return {
        "category": category,
        "max_price": max_price,
        "min_price": min_price,
        "in_stock": in_stock,
        "order_by": order_by,
        "limit": limit,
    }


# Query() & Path() — validates & adds metadata to query params, avoids manual checks
# skipping it means no constraints and incomplete docs
# limit: int = Query(..., default=10, ge=1, le=100), => (...) means this query param is required
@router.get("/products")
def get_products(
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, min_length=3, max_length=50),
):
    return {"limit": limit, "search": search}


@router.get("/users/{user_id}/posts")
def get_posts(
    user_id: int = Path(..., ge=1),
    limit: int = Query(10, le=50),
    search: str | None = Query(None, min_length=3),
):
    return {"user_id": user_id, "limit": limit, "search": search}
