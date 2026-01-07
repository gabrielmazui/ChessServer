import time, secrets
from app.storage import sessions

def create_session(username: str, SESSION_TIME: int = 60 * 60):
    token = secrets.token_hex(32)
    sessions[token] = {
        "user": username,
        "exp": time.time() + SESSION_TIME
    }
    return token


def get_user_from_session(token: str | None):
    if not token:
        return None

    data = sessions.get(token)
    if not data:
        return None

    if data["exp"] < time.time():
        sessions.pop(token, None)
        return None

    return data["user"]
