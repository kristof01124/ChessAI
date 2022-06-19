class Pieces:
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6


class Directions:
    directions = [
        -9, -8, -7,
        -1,  0,  1,
        7,  8,  9
    ]

    knightDirections = [
        -9 - 1, -9 - 8,
        -7 - 8, - 7 + 1,
        9 + 1, 9 + 8,
        7 - 1, 7 + 8
    ]


class Inside:
    inside = [
        [
            i + Directions.directions[j] >= 0 and i + Directions.directions[j] < 64 and abs(i / 8 - (i + Directions.directions[j])/8) < 2 and
            abs((i % 8) - ((i + Directions.directions[j] % 8)) < 2)
            for j in range(0, 9)
        ]
        for i in range(0, 64)
    ]

    insideKnight = [
        [
            
        ]
    ]

class Board:
    def __init__(self):
        pass

    #public

    def importBoard(self, board, castling  = None, moveHistory = None, white = True):
        if castling is None:
            castling = [False, False, False, False]
        if moveHistory is None:
            moveHistory = []
        self.checks = 0
        self.white = white
        self.board = board
        self.castling = castling
        self.moveHistory = moveHistory
        self.possibleMoves = []
        self.dangerMap = [[0 for i in range(0,8)] for j in range(0,8)]

    def clear(self):
        self.possibleMoves.clear()
        self.dangerMap.clear()

    def makeMove(self, move): # return the move object
        pass

    def reverseMove(self, move): # return nothing
        pass

    def getAllPossibleMoves(self):
        self.clear()
        self.__generateDangerMap()
        self.__getCastleMoves()
        self.__getEnPassantMoves()
        for i in range(0, 64):
            if self.__withMe(i):
                match self.board[i]:
                    case Pieces.PAWN:
                        self.__getPawnMoves(i)
                    case Pieces.KNIGHT:
                        self.__getKnightMoves(i)
                    case Pieces.BISHOP:
                        self.__getBishopMoves(i)
                    case Pieces.ROOk:
                        self.__getRookMoves(i)
                    case Pieces.QUEEN:
                        self.__getQueenMoves(i)
                    case Pieces.KING:
                        self.__getKingMoves(i)
        self.__validateMoves()

    #private

    #helper functions

    def __findKings(self):
        pass

    def __inside(self, frm, mv):
        pass

    def __withMe(self, poz):
        pass

    def __withEnemey(self, poz):
        pass

    def __getOffset(self, dir):
        pass

    #danger map generation

    def __generateDangerMap(self):
        for i in range(0, 64):
            if self.__withEnemey(i):
                match self.board[i]:
                    case Pieces.PAWN:
                        self.__dangerMapPawn(i)
                    case Pieces.KNIGHT:
                        self.__dangerMapKnight(i)
                    case Pieces.BISHOP:
                        self.__dangerMapBishop(i)
                    case Pieces.ROOk:
                        self.__dangerMapRook(i)
                    case Pieces.QUEEN:
                        self.__dangerMapQueen(i)
                    case Pieces.KING:
                        self.__dangerMapKing(i)

    def __dangerMapHandleSliding(self, poz, dir):
        pass

    def __dangerMapBishop(self, poz):
        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                self.__dangerMapHandleSliding(poz, i * 3 + j)

    def __dangerMapRook(self, poz):
        for i in range(-1, 2):
            for j in range(-1, 2):
                if abs(i) + abs(j) == 1:
                    self.__dangerMapHandleSliding(poz, i * 3 + j)

    def __dangerMapQueen(self, poz):
        for i in range(0, 9):
            if i != 4:
                self.__dangerMapHandleSliding(poz, i)

    def __dangerMapKing(self, poz):
        for j in range(0, 9):
            if Inside.inside[poz][j]:
                self.dangerMap[poz + Directions.directions[j]] += 1


    def __dangerMapPawn(self, poz):
        if self.white:
            dir = 0
        else:
            dir = 6
        for j in range(dir, dir+3, 2):
            if Inside.inside[poz][j]:
                to = poz + Directions.directions[j]
                self.dangerMap[to] = +1
                if self.__withMe(to) and abs(self.board[to]) == Pieces.KING:
                    checks += 1



    def __dangerMapEnPassant(self, poz):
        pass

    def __dangerMapKnight(self, poz):


    # possible move search

    def __getCastleMoves(self):
        pass

    def __getEnPassantMoves(self):
        pass

    def __getSlidemoves(self, poz, dir = 4):
        pass

    def __getRookMoves(self, poz, dir = 4):
        pass

    def __getBishopMoves(self, poz, dir = 4):
        pass

    def __getKingMoves(self, poz, dir = 4):
        pass

    def __getQueenMoves(self, poz, dir = 4):
        pass

    def __getPawnMoves(self, poz, dir = 4):
        pass

    def __getKnightMoves(self, poz, dir = 4):
        pass



