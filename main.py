from fastapi import FastAPI, Request
from routers import users, products

app = FastAPI(title="My API", version="1.0.0", description="FastAPI project")


@app.middleware("http")
async def simple_middleware(request: Request, call_next):
    response = await call_next(request)
    print(f"message from the middleware {request.method}{request.url.path} -> {response.status_code}")
    return response

app.include_router(users.router)
app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "App is running"}
