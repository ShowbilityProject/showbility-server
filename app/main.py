from fastapi import FastAPI
from app.routers import users
from app.db.init_db import init_db

app = FastAPI()

app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.get("/")
async def main():
    return {"hello": "showbility"}
