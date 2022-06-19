class Pieces:
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Directions:
    directions = [
        [-9, -8, -7],
        [-1,  0,  1],
        [ 7,  8,  9]
    ]


class Inside:
    inside = [
        [
            [i + Directions.directions[j][k] >= 0 and i + Directions.directions[j][k] < 64 and abs(i / 8 - (i + Directions.directions[j][k])/8) <= 1 and
            abs((i % 8) - ((i + Directions.directions[j][k]) % 8)) <= 1 for k in range(0, 3)]
            for j in range(0, 3)
        ]
        for i in range(0, 64)
    ]

class Board:
    def __init__(self):
        pass

    #public

    def makeMove(self, move): # return the move object
        pass

    def reverseMove(self, move): # return nothing
        pass

    def getAllPossibleMoves(self):
        pass

    #private

    #helper functions

    def __findKings(self):
        pass

    def inside(self, frm, mv):
        pass

    def withMe(self, poz):
        pass

    def withEnemey(self, poz):
        pass

    #danger map generation

    def __generateDangerMap(self, poz):
        pass

    def __dangerMapHandleSliding(self, poz, dir):
        pass

    def __dangerMapBishop(self, poz):
        pass

    def __dangerMapRook(self, poz):
        pass

    def __dangerMapQueen(self, poz):
        pass

    def __dangerMapKing(self, poz):
        pass

    def __dangerMapPawn(self, poz):
        pass

    def __dangerMapEnPassant(self, poz):
        pass




