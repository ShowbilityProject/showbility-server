from fastapi import FastAPI, Depends
from app.db.init_db import init_db
from app.api.routers import users
from app.api.routers import auth
from starlette.staticfiles import StaticFiles
from fastapi.security.api_key import APIKeyHeader

auth_header = APIKeyHeader(name="Authorization", auto_error=False)
app = FastAPI(dependencies=[Depends(auth_header)])

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.on_event("startup")
def startup_event():
    init_db()

@app.get("/")
def main():
    return {"hello": "showbility"}
