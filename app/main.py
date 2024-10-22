from fastapi import FastAPI, Depends
from app.db.init_db import init_db
from app.api.routers import users
from starlette.staticfiles import StaticFiles

app = FastAPI()

app.include_router(users.router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def main():
    return {"hello": "showbility"}
