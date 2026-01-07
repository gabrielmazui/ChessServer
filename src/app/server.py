from fastapi import FastAPI, StaticFiles
from app.routes import auth, home, match

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(home.router)
app.include_router(match.router)
