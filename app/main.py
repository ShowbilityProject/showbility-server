from fastapi import FastAPI
from app.routers import users
import app.db

app = FastAPI()

app.include_router(users.router)

@app.get("/")
async def main():
    return {"hello": "showbility"}
