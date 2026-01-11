from fastapi import APIRouter,WebSocket, WebSocketDisconnect, Cookie
from app.storage import *
import asyncio

match_lock = asyncio.Lock()

router = APIRouter(tags=["ws"])

@router.websocket("/ws/match/{match_id}")
async def ws_match(
    websocket: WebSocket,
    match_id: str,
    session: str | None = Cookie(default=None)
):
    await websocket.accept()

    ses = sessions.get(session)
    
    if ses == None:
        await websocket.send_json({
            "type": "error",
            "content": "user does not exist"
        })
        await websocket.close()
        return

    match = None
    
    usr = ses.get("user")
    
    async with match_lock:
        if match_id in waiting_matches:
            if match.players["white"] != usr:
                #verificando se e o usuario que criou a match
                match = waiting_matches.pop(match_id)
                m = waiting_matches_http.pop(match_id)

                matches[match_id] = match

                m.players[1] = usr
                matches_http[match_id] = m
            else:
                match = waiting_matches[match_id]
        elif match_id in matches:
            match = matches[match_id]
        

    if match == None:
        # partida nao existe
        await websocket.send_json({
            "type": "error",
            "content": "match does not exist"
        })
        await websocket.close()
        return
    
    match.connections.append(websocket)

    player = False # se e jogador ou spectador
    
    if match.players["white"] == usr:
        # valor dado quando /create-match
        player = True
    elif match.players["black"] == None:
        # vai ser jogador
        player = True
        match.players["black"] = usr
        match.status = "playing"

    if not player:
        match.spectators += 1

    try:
        while True:
            data = await websocket.receive_json()
            type = data.get("type", None)

            if type == "move":
                if match.status == "waiting":
                    await websocket.send_json({
                        "type": "error",
                        "content": "waiting for a player to join the match"
                    })
                    continue

                elif match.status == "finished":
                    await websocket.send_json({
                        "type": "error",
                        "content": "this game already finished"
                    })
                    continue

                if not player:
                    await websocket.send_json({
                        "type": "error",
                        "content": "you are not a player"
                    })
                    continue

                turn = match.engine.turn
                if match.players[turn] == usr:
                    fr = data.get("fr", None)
                    fc = data.get("fc", None)
                    tr = data.get("tr", None)
                    tc = data.get("tc", None)
                    if fr == None or fc == None or tr == None or tc == None:
                        await websocket.send_json({
                            "type": "error",
                            "content": "error while reading positions"
                        })
                        continue

                    if match.engine.move((fr, fc), (tr, tc)):
                        # brodcast
                        for ws in list(match.connections):
                            try:
                                await ws.send_json({
                                    "type": "move",
                                    "board": match.engine.board,
                                    "turn": match.engine.turn,
                                    "check": match.engine.is_in_check(match.engine.turn),
                                    "checkmate": match.engine.is_checkmate(match.engine.turn)
                                })
                            except:
                                match.connections.remove(ws)
                                
                    else:
                        await websocket.send_json({
                            "type": "error",
                            "content": "could not move that"
                        })
                        continue
                else:   
                    await websocket.send_json({
                        "type": "error",
                        "content": "it is not your turn"
                    })
                    continue

                await websocket.send_json({
                    "type": "error",
                    "content": "could not move that"
                })
    except WebSocketDisconnect:
        #verificar se era jogador
        if websocket in match.connections:
            match.connections.remove(websocket)

        if not player:
            match.spectators -= 1
        else:
            if match.players["dark"] == None:
                # a partida nem comecou
                waiting_matches.pop(match_id, None)
                waiting_matches_http.pop(match_id, None)
                return
            
            match.status = "finished"
            winner = "unknown" 
            if match.players["white"] == player:
                sess = sessions.get(match.players["dark"])
                if sess != None:
                    winner = sess.get("user")

            elif match.players["dark"] == player:
                sess = sessions.get(match.players["white"])
                if sess != None:
                    winner = sess.get("user")

            if winner == None:
                winner = "Unknown"
            # brodcast
            for ws in list(match.connections):
                try:
                    await ws.send_json({
                        "type": "end",
                        "winner": winner
                    })
                    ws.close()
                except:
                    match.connections.remove(ws)

            matches.pop(match_id, None)
            matches_http.pop(match_id, None)
            #partida acabou
            
        return