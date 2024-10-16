from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.routers import users

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def main():
    return {"hello": "showbility"}