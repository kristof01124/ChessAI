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


class Moves:
    Bishop = [[0, 0], [0, 2], [2, 0], [2, 2]]
    Rook = [[0, 1], [1, 0], [1, 2], [2, 1]]
    King = list([j, i] for i in range(0, 3) for j in range(0,3, 2)) + [[1, 0], [1, 2]]
    BlackPawn = [[0, 0], [0, 2]]
    WhitePawn = [[2, 2], [2, 0]]

class Inside:
    inside = [
        [
            [
            i + Directions.directions[j][k] >= 0 and
            i + Directions.directions[j][k] < 64 and
            int(((i+Directions.directions[j][k]))/8) - int(i/8)  == j - 1 and
            (i + Directions.directions[j][k])%8 - (i % 8) == k - 1
            for k in range(0, 3)
            ]
            for j in range(0, 3)
        ]
        for i in range(0, 64)
    ]



class KnightMoves:
    directions = [
        Directions.directions[i][j] + Directions.directions[k[0]][k[1]] for i in range(0, 3, 2) for j in range(0, 3, 2) for k in [[i ,1], [1, j]]
    ]

    inside = [[
         Inside.inside[poz][i][j] and Inside.inside[poz + Directions.directions[i][j]][k[0]][k[1]] for i in range(0, 3, 2) for j in range(0, 3, 2) for k in [[i, 1], [1, j]]
    ] for poz in range(0, 64)
    ]



class Board:
    def __init__(self):
        self.__dangerMap = [0 for i in range(0,64)]
        self.state = [0 for i in range(0, 64)]
        self.__castling = [False, False, False, False]
        self.__moveHistory = []
        self.white = True

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
        return self.white and self.state[poz] > 0 or not self.white and self.state[poz] < 0

    def withEnemey(self, poz):
        return self.white and self.state[poz] < 0 or not self.white and self.state[poz] > 0

    #danger map generation

    def generateDangerMap(self):
        for i in self.__dangerMap:
            i = 0
        for i in range(0, 64):
            if self.withEnemey(i):
                match abs(self.state[i]):
                    case Pieces.KING:
                        self.__dangerMapKing(i)
                    case Pieces.KNIGHT:
                        self.__dangerMapKnight(i)
                    case Pieces.PAWN:
                        self.__dangerMapPawn(i)
        for i in range(0, 64):
            if self.withEnemey(i):
                match abs(self.state[i]):
                    case Pieces.ROOK:
                        self.__dangerMapRook(i)
                    case Pieces.BISHOP:
                        self.__dangerMapBishop(i)
                    case Pieces.QUEEN:
                        self.__dangerMapQueen(i)





    def __dangerMapHandleSliding(self, poz, dir):
        move = Directions.directions[dir[0]][dir[1]]
        pinnedPiece = 0
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            if self.withMe(poz):
                if pinnedPiece > -1:
                    if abs(self.state[poz]) == Pieces.KING:
                        self.__handlePin(pinnedPiece, [2 - dir[0], 2 - dir[1]])
                    else:
                        return
                pinnedPiece = poz
            if self.withEnemey(poz):
                return
            if pinnedPiece > -1:
                return
            if self.__dangerMap[poz] == 0:
                self.__dangerMap[poz] = 1

    def __handlePin(self, poz, dir):
        move = Directions.directions[dir[0]][dir[1]]
        poz += move
        while not self.withMe(poz):
            self.__dangerMap[poz] = 2
            poz += move


    def __dangerMapBishop(self, poz):
        for i in Moves.Bishop:
            self.__dangerMapHandleSliding(poz, i)

    def __dangerMapRook(self, poz):
        for i in Moves.Rook:
            self.__dangerMapHandleSliding(poz, i)

    def __dangerMapQueen(self, poz):
        self.__dangerMapBishop(poz)
        self.__dangerMapBishop(poz)

    def __dangerMapKing(self, poz):
        for i in Moves.King:
            if Inside.inside[poz][i[0]][i[1]]:
                self.__dangerMap[poz + Directions.directions[i[0]][i[1]]] = 1


    def __dangerMapPawn(self, poz):
        if not self.white:
            l = Moves.WhitePawn
        else:
            l = Moves.BlackPawn
        for j in l:
            if Inside.inside[poz][j[0]][j[1]]:
                self.__dangerMap[poz + Directions.directions[j[0]][j[1]]] = 1

    def __dangerMapKnight(self, poz):
        for i in range(0, 8):
            if KnightMoves.inside[poz][i]:
                self.state[poz + KnightMoves.directions[[i]]] = 1




