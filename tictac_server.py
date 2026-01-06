from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Cookie
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uuid
import uvicorn

waiting_matches = {} 
matches = {}
ia_matches = {}
# id -> json do match

users = {} # id -> user

# id
# status (waiting), (playing) #### o waiting pode estar esperando para o usuario abrir conexao ws
# spectators
# user1
# user2
# user1Id
# user2Id
# rounds
# betterOf
# turn
# p1
# p2

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/match", StaticFiles(directory="static/match"), name="match")

#---------------
#GERAL
@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()
    
@app.get("/match", response_class=HTMLResponse)
def match():
    with open("static/match/index.html", encoding="utf-8") as f:
        return f.read()

#---------------
# CREATE MATCHES
@app.post("/create-math-player")
async def create_match_player(request: Request, player_id: str | None = Cookie(default = None)):
    data = await request.json() # BOF
    if player_id == None:
        #envia pro login
        pass
    
    match_wait = {}
    match_wait["user1id"] = player_id
    match_wait["user1"] = users.get(player_id)
    match_wait["bof"] = data.get("bof")
    match_wait["status"] = "waiting"
    match_id = str(uuid.uuid4())

    #ia e em local diferente entao nao precisa ser verificado aqui
    while match_id in matches or match_id in waiting_matches:
        match_id = str(uuid.uuid4())
    match_wait["id"] = match_id
    waiting_matches[match_id] = match_wait

    return match_wait
    
@app.post("/create-math-ia")
async def create_match_ia(request: Request, player_id: str | None = Cookie(default = None)):
    data = await request.json() # BOF
    if player_id == None:
        #envia pro login
        pass
    
    match_ia = {}
    match_ia["user1id"] = player_id
    match_ia["user1"] = users.get(player_id)
    match_ia["p1"] = 0
    match_ia["user2"] = "mazui" # nomes aleatorios de ia depois
    match_ia["p2"] = 0

    match_ia["bof"] = data.get("bof")
    match_ia["rounds"] = 0
    match_ia["turn"] = "x"

    match_ia["user1type"] = "x"
    match_ia["user2type"] = "o"

    match_ia["status"] = "waiting"
    match_id = str(uuid.uuid4())

    while match_id in ia_matches:
        match_id = str(uuid.uuid4())
    match_ia["id"] = match_id
    waiting_matches[match_id] = match_ia

    return match_ia

# ----------
# JOIN MATCH
@app.post("/join-match")
async def create_match_ia(request: Request, player_id: str | None = Cookie(default = None)):
    data = await request.json() # BOF
    if player_id == None:
        #envia pro login
        pass
    
    match_from_waiting_id = data.get("id")    

    match_from_waiting = waiting_matches[match_from_waiting_id]

    match = {}
    match["user1id"] = match_from_waiting.get("user1id")
    match["user1"] = match_from_waiting.get("user1")
    match["p1"] = 0

    match["user2id"] = player_id
    match["user2"] = users.get(player_id) # nomes aleatorios de ia depois
    match["p2"] = 0
    
    match["bof"] = data.get("bof")
    match["rounds"] = 0
    match["turn"] = "x"

    match["user1type"] = "x"
    match["user2type"] = "o"

    match["status"] = "waiting"
    match["spectators"] = 0

    match_id = match_from_waiting.get("id")

    matches[match_id] = match
    waiting_matches.pop(match_id, None)

    return match
uvicorn.run(app, host="0.0.0.0", port=8080)