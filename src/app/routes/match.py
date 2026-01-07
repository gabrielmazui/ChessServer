from fastapi import APIRouter, Request, Cookie
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import uuid
from app.auth.session import *
from app.storage import *
app = APIRouter()

templates = Jinja2Templates(directory="app/templates")

#---------------
# CREATE MATCHES
@app.post("/create-math-player")
async def create_match_player(request: Request, session: str | None = Cookie(default = None)):
    data = await request.json() # BOF
    if get_user_from_session(session) == None:
        response = RedirectResponse(
            url="/",
            status_code=303
        )
        return response
    
    match_wait = {
        "user1id": session,
        "user1": users.get(session),
        "bof": data.get("bof"),
        "status": "waiting"
    }

    match_id = str(uuid.uuid4())

    #ia e em local diferente entao nao precisa ser verificado aqui
    while match_id in matches or match_id in waiting_matches:
        match_id = str(uuid.uuid4())
    match_wait["id"] = match_id
    waiting_matches[match_id] = match_wait

    return match_wait
    
@app.post("/create-math-ia")
async def create_match_ia(request: Request, session: str | None = Cookie(default = None)):
    data = await request.json() # BOF
    if get_user_from_session(session) == None:
        response = RedirectResponse(
            url="/",
            status_code=303
        )
        return response
    
    match_ia = {
        "user1id": session,
        "user1": users.get(session),
        "p1": 0,
        "user2": "mazui", # nomes aleatorios de ia depois
        "p2": 0,
        "bof": data.get("bof", 5),
        "rounds": 0,
        "turn": "x",
        "user1type": "x",
        "user2type": "o",
        "status": "waiting"
    }
   
    match_id = str(uuid.uuid4())

    while match_id in ia_matches:
        match_id = str(uuid.uuid4())
    match_ia["id"] = match_id
    waiting_matches[match_id] = match_ia

    return match_ia

# ----------
# JOIN MATCH
@app.get("/match/{game_session}", response_class=HTMLResponse)
async def create_match_ia(request: Request, session: str | None = Cookie(default = None)):
    data = await request.json() 
    if get_user_from_session(session) == None:
        response = RedirectResponse(
            url="/",
            status_code=303
        )
        return response
    
    if not match:
        return templates.TemplateResponse(
            "match_not_found.html",
            {
                "request": request,
                "match_id": match_id
            }
        )
    
    match_from_waiting_id = data.get("id")    

    match_from_waiting = waiting_matches[match_from_waiting_id]
    #contiunua
    match = {
        "user1id": match_from_waiting.get("user1id"),
        "user1": users.get(session),
        "p1": 0,
        "user2": "mazui", # nomes aleatorios de ia depois
        "p2": 0,
        "bof": data.get("bof", 5),
        "rounds": 0,
        "turn": "x",
        "user1type": "x",
        "user2type": "o",
        "status": "waiting",
        "spectators": 0
    }

    match_id = match_from_waiting.get("id")

    matches[match_id] = match
    waiting_matches.pop(match_id, None)

    return match