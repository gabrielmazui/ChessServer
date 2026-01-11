from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth, home, match, websocket

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(match.router)
app.include_router(websocket.router)