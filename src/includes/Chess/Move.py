class Move:
    def __init__(self, frm, to, captured = 0, castles = None, enPassant = False):
        self.frm = frm
        self.to = to
        self.captured = captured
        self.castles = castles
        self.enPassant = enPassant

    def converToAlgebraicNotation(self):
        pass