import copy

WHITE = "white"
BLACK = "black"

class ChessEngine:
    def __init__(self):
        self.board = self._initial_board()
        self.turn = WHITE
        self.move_history = []
        self.en_passant = None  # (row, col)
        self.moved = {
            "K": False, "k": False,
            "Ra": False, "Rh": False,
            "ra": False, "rh": False,
        }

    # =====================
    # BOARD
    # =====================
    def _initial_board(self):
        return [
            ["r","n","b","q","k","b","n","r"],
            ["p","p","p","p","p","p","p","p"],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["","","","","","","",""],
            ["P","P","P","P","P","P","P","P"],
            ["R","N","B","Q","K","B","N","R"],
        ]

    # =====================
    # PUBLIC MOVE
    # =====================
    def move(self, f, t, promotion=None):
        fr, fc = f
        tr, tc = t
        piece = self.board[fr][fc]

        if not piece:
            return False

        if self.turn == WHITE and not piece.isupper():
            return False
        if self.turn == BLACK and not piece.islower():
            return False

        snapshot = copy.deepcopy(self)

        if not self._valid_move(piece, f, t):
            return False

        self._apply_move(f, t, promotion)

        if self.is_in_check(snapshot.turn):
            self.__dict__ = snapshot.__dict__
            return False

        self.turn = BLACK if self.turn == WHITE else WHITE
        return True

    # =====================
    # APPLY MOVE
    # =====================
    def _apply_move(self, f, t, promotion):
        fr, fc = f
        tr, tc = t
        piece = self.board[fr][fc]

        # en passant capture
        if piece.lower() == "p" and self.en_passant == (tr, tc):
            self.board[fr][tc] = ""

        self.board[tr][tc] = piece
        self.board[fr][fc] = ""

        # promotion
        if piece.lower() == "p" and (tr == 0 or tr == 7):
            self.board[tr][tc] = promotion or ("Q" if piece.isupper() else "q")

        # roque
        if piece.lower() == "k" and abs(tc - fc) == 2:
            if tc > fc:  # curto
                self.board[tr][5] = self.board[tr][7]
                self.board[tr][7] = ""
            else:  # longo
                self.board[tr][3] = self.board[tr][0]
                self.board[tr][0] = ""

        # en passant target
        self.en_passant = None
        if piece.lower() == "p" and abs(tr - fr) == 2:
            self.en_passant = ((fr + tr)//2, fc)

        # moved flags
        if piece in self.moved:
            self.moved[piece] = True
        if piece == "R" and fr == 7 and fc == 0: self.moved["Ra"] = True
        if piece == "R" and fr == 7 and fc == 7: self.moved["Rh"] = True
        if piece == "r" and fr == 0 and fc == 0: self.moved["ra"] = True
        if piece == "r" and fr == 0 and fc == 7: self.moved["rh"] = True

        self.move_history.append((f, t, piece))

    # =====================
    # CHECK
    # =====================
    def is_in_check(self, color):
        king = "K" if color == WHITE else "k"
        kr, kc = self._find(king)

        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p and p.isupper() != king.isupper():
                    if self._valid_move(p, (r,c), (kr,kc), ignore_check=True):
                        return True
        return False

    # =====================
    # MOVE VALIDATION
    # =====================
    def _valid_move(self, piece, f, t, ignore_check=False):
        target = self.board[t[0]][t[1]]
        if target and target.isupper() == piece.isupper():
            return False

        p = piece.lower()
        if p == "p": return self._pawn(piece, f, t)
        if p == "r": return self._rook(f, t)
        if p == "n": return self._knight(f, t)
        if p == "b": return self._bishop(f, t)
        if p == "q": return self._queen(f, t)
        if p == "k": return self._king(piece, f, t)
        return False

    # =====================
    # PIECES
    # =====================
    def _pawn(self, piece, f, t):
        fr, fc = f
        tr, tc = t
        d = -1 if piece.isupper() else 1
        start = 6 if piece.isupper() else 1

        if fc == tc and self.board[tr][tc] == "":
            if tr == fr + d:
                return True
            if fr == start and tr == fr + 2*d and self.board[fr+d][fc] == "":
                return True

        if abs(tc-fc)==1 and tr==fr+d:
            if self.board[tr][tc] != "":
                return True
            if self.en_passant == (tr, tc):
                return True

        return False

    def _rook(self, f, t):
        return (f[0]==t[0] or f[1]==t[1]) and self._path_clear(f,t)

    def _bishop(self, f, t):
        return abs(f[0]-t[0])==abs(f[1]-t[1]) and self._path_clear(f,t)

    def _queen(self, f, t):
        return self._rook(f,t) or self._bishop(f,t)

    def _knight(self, f, t):
        return (abs(f[0]-t[0]), abs(f[1]-t[1])) in [(1,2),(2,1)]

    def _king(self, piece, f, t):
        fr, fc = f
        tr, tc = t

        if abs(fr-tr)<=1 and abs(fc-tc)<=1:
            return True

        # roque
        if piece.isupper():
            if self.moved["K"]: return False
            if tc == 6 and not self.moved["Rh"]:
                return self._path_clear((7,4),(7,7))
            if tc == 2 and not self.moved["Ra"]:
                return self._path_clear((7,4),(7,0))
        else:
            if self.moved["k"]: return False
            if tc == 6 and not self.moved["rh"]:
                return self._path_clear((0,4),(0,7))
            if tc == 2 and not self.moved["ra"]:
                return self._path_clear((0,4),(0,0))

        return False

    # =====================
    # UTILS
    # =====================
    def _path_clear(self, f, t):
        fr,fc = f
        tr,tc = t
        dr = (tr-fr) and (1 if tr>fr else -1)
        dc = (tc-fc) and (1 if tc>fc else -1)
        r,c = fr+dr, fc+dc
        while (r,c)!=(tr,tc):
            if self.board[r][c]:
                return False
            r+=dr; c+=dc
        return True

    def _find(self, piece):
        for r in range(8):
            for c in range(8):
                if self.board[r][c]==piece:
                    return r,c
        raise ValueError("piece not found")