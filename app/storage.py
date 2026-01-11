from app.chess.chess_match import ChessMatch
from app.chess.chess_match_http import ChessMatchHttp

waiting_matches: dict[str, ChessMatch] = {} 
matches: dict[str, ChessMatch] = {}

waiting_matches_http: dict[str, ChessMatchHttp]
matches_http: dict[str, ChessMatchHttp]
# para enviar para o cliente

# id -> class do match

users: dict[str, dict[str, str]] = {}      # username -> { password }
sessions: dict[str, dict] = {}   # token -> { user, exp }