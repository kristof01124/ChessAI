class Move:
    def __init__(self, frm, to, captured = 0, brokenCastles = None, enPassant = False):
        self.frm = frm
        self.to = to
        self.captured = captured
        self.brokentCastles = brokenCastles
        self.enPassant = enPassant

    def converToAlgebraicNotation(self):
        pass