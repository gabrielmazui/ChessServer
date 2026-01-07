from fastapi import APIRouter, HTMLResponse, StaticFiles
from fastapi.responses import HTMLResponse

app = APIRouter()

#---------------
#HTMLResponse
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/home.html", encoding="utf-8") as f:
        return f.read()
    
@app.get("/match", response_class=HTMLResponse)
def match():
    with open("templates/match.html", encoding="utf-8") as f:
        return f.read()

@app.get("/login", response_class=HTMLResponse)
def match():
    with open("templates/login.html", encoding="utf-8") as f:
        return f.read()