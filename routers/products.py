from fastapi import APIRouter, Query

router = APIRouter(prefix="/products", tags=["Products"])

# Query() and Path() add validation + richer OpenAPI docs.
# Query(...) with ellipsis means the param is required (no default).


@router.get("/")
def get_products(
    limit: int = Query(default=10, ge=1, le=100),
    search: str | None = Query(default=None, min_length=3, max_length=50),
):
    return {"limit": limit, "search": search}


@router.get("/{category}")
def get_products_by_category(
    category: str,
    max_price: int = Query(...),
    min_price: int = Query(...),
    in_stock: bool = Query(default=True),
    order_by: str = Query(default="price"),
    limit: int = Query(default=10, ge=1, le=100),
):
    return {
        "category": category,
        "max_price": max_price,
        "min_price": min_price,
        "in_stock": in_stock,
        "order_by": order_by,
        "limit": limit,
    }
