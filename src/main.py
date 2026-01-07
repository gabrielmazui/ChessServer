from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, Cookie, Form, HTTPException, Response, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uuid

import uvicorn
from app.auth.session import create_session, get_user_from_session


app = FastAPI()






uvicorn.run(app, host="0.0.0.0", port=8080)