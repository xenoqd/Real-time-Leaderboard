from fastapi import FastAPI

from backend.db.session import init_db
from backend.api.v1.auth.auth import auth_router

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await init_db()


app.include_router(auth_router)
