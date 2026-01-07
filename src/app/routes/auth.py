from fastapi import APIRouter, Cookie, Form, HTTPException, Response
from fastapi.responses import RedirectResponse
from passlib.context import CryptContext
from app.auth.session import *
from app.storage import *

app = APIRouter()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

#-------------
# SIGNUP
@app.post("/signup")
def signup(
    username: str = Form(..., min_length=3),
    password: str = Form(..., min_length=6)
):
    if username in users:
        raise HTTPException(400, "Não foi possível criar a conta")

    users[username] = {
        "password": pwd.hash(password)
    }

    response = RedirectResponse(
        url="/",
        status_code=303
    )
    return response


@app.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    keeplogged: str | None = Form(None)
):
    user = users.get(username)

    if not user or not pwd.verify(password, user["password"]):
        raise HTTPException(401, "Usuário ou senha inválidos")

    session_time = 60 * 60           # 1 hora
    if keeplogged:
        session_time = 60 * 60 * 24 * 7  # 7 dias
    token = create_session(username, session_time)

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    response.set_cookie(
        key="session",
        value=token,
        httponly=True,
        samesite="lax"
    )
    
    return response

@app.post("/logout")
def logout(
    response: Response,
    session: str | None = Cookie(None)
):
    if session:
        sessions.pop(session, None)

    response = RedirectResponse(
        url="/",
        status_code=303
    )

    response.delete_cookie("session")
    return {"ok": True, "msg": "Logout feito"}
