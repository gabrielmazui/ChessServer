from fastapi import APIRouter, Cookie, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.storage import *
templates = Jinja2Templates(directory="app/templates")

router = APIRouter(tags=["home"])

#---------------
#HTMLResponse
@router.get("/")
def home(request: Request, session: str | None = Cookie(None)):
    ses = sessions.get(session)
    # if ses == None:
    #     response = RedirectResponse(
    #         url="/login",
    #         status_code=303
    #     )

    # else:

    # usr = ses.get("user") 
    response = templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "username": "teste",
            "waiting_matches": waiting_matches,
            "running_matches": matches
        }
    )
    return response

@router.get("/login", response_class=HTMLResponse)
def match():
    with open("templates/login.html", encoding="utf-8") as f:
        return f.read()
    
@router.get("/signup", response_class=HTMLResponse)
def match():
    with open("templates/signup.html", encoding="utf-8") as f:
        return f.read()