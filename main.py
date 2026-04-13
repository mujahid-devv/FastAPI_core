from fastapi import FastAPI
from routers import users
app = FastAPI(title="My API", version="1.0.0", description="FastAPI project")

app.include_router(users.router)

@app.get("/")
def root():
    return {"message":"app is running"}