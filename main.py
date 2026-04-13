from fastapi import FastAPI
from routers import users, products

app = FastAPI(title="My API", version="1.0.0", description="FastAPI project")

app.include_router(users.router)
app.include_router(products.router)


@app.get("/")
def root():
    return {"message": "App is running"}
