from fastapi import WebSocket
from typing import List
from app.chess.engine import ChessEngine

class ChessMatch:
    def __init__(self, white_player, black_player):
        self.players = {
            "white": white_player,
            "black": black_player
        }
        self.status = "playing"  # waiting | playing | finished
        self.connections: List[WebSocket] = []
        self.engine = ChessEngine()
        self.spectators = 0