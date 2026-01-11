class ChessMatchHttp:
    def __init__(self, token : str, usr1: str, usr2: str | None = None):
        self.players = [usr1, usr2]
        self.id = token