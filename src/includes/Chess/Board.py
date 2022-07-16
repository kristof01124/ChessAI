import copy


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
    BlackPawnCapture = [[0, 0], [0, 2]]
    BlackPawnAdvance = [0, 1]
    BlackPawn = [[0, 0], [0, 1], [0, 2]]
    WhitePawnCapture = [[2, 2], [2, 0]]
    WhitePawn = [[2, 0], [2, 1], [2, 2]]
    WhitePawnAdvance = [2, 1]


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
        self.__possibleMoves = []
        self.__dangerMap = [0 for i in range(0,64)]
        self.state = [0 for i in range(0, 64)]
        self.__castling = [False, False, False, False]
        self.__moveHistory = []
        self.white = True
        self.__checks = 0

    #public

    def makeMove(self, move): # return the move object
        pass

    def reverseMove(self, move): # return nothing
        pass

    def getAllPossibleMoves(self):
        self.generateDangerMap()
        for i in range(0, 64):
            if self.withMe(i):
                match abs(self.state[i]):
                    case Pieces.KING:
                        self.__getPossibleKingMoves(i)
                    case Pieces.QUEEN:
                        self.__getPossibleQueenMoves(i)
                    case Pieces.BISHOP:
                        self.__getPossibleBishopMoves(i)
                    case Pieces.KNIGHT:
                        self.__getPossibleKnightMoves(i)
                    case Pieces.ROOK:
                        self.__getPossibleRookMoves(i)
                    case Pieces.PAWN:
                        self.__getPossiblePawnMoves(i)
        print(len(self.__possibleMoves))

    #private

    def __getPossibleKingMoves(self, poz):
        for j in Moves.King:
            if Inside.inside[poz][j[0]][j[1]] and self.__dangerMap[poz + Directions.directions[j[0]][j[1]]] == 0 and not self.withMe(poz + Directions.directions[j[0]][j[1]]):
                self.__possibleMoves.append([poz, poz + Directions.directions[j[0]][j[1]]])


    def __getPossibleKnightMoves(self, poz):
        for i in range(0, 8):
            if KnightMoves.inside[poz][i] and not self.withMe(poz + KnightMoves.directions[i]):
                self.__possibleMoves.append([poz, poz + KnightMoves.directions[i]])

    def __getPossibleBishopMoves(self, poz):
        for dir in Moves.Bishop:
            self.__addSlideToPossibleMoves(poz, dir)

    def __getPossibleQueenMoves(self, poz):
        self.__getPossibleBishopMoves(poz)
        self.__getPossibleRookMoves(poz)

    def __getPossibleRookMoves(self, poz):
        for dir in Moves.Rook:
            self.__addSlideToPossibleMoves(poz, dir)

    def __getPossiblePawnMoves(self, poz):
        if self.white:
            capture = Moves.WhitePawnCapture
            advance = Moves.WhitePawnAdvance
        else:
            capture = Moves.BlackPawnCapture
            advance = Moves.BlackPawnAdvance
        for i in capture:
            if Inside.inside[poz][i[0]][i[1]] and self.withEnemey(poz + Directions.directions[i[0]][i[1]]):
                self.__possibleMoves.append([poz, poz + Directions.directions[i[0]][i[1]]])
        if Inside.inside[poz][advance[0]][advance[1]] and self.state[poz + Directions.directions[advance[0]][advance[1]]] == 0:
            self.__possibleMoves.append([poz, poz + Directions.directions[advance[0]][advance[1]]])
            if Inside.inside[poz + Directions.directions[advance[0]][advance[1]]][advance[0]][advance[1]] and \
                self.state[poz + Directions.directions[advance[0]][advance[1]] + Directions.directions[advance[0]][advance[1]]] == 0:
                self.__possibleMoves.append([poz, poz + Directions.directions[advance[0]][advance[1]] + Directions.directions[advance[0]][advance[1]]])



    def __getCastleMoves(self, poz):
        pass

    def __getEnPassantMoves(self, poz):
        pass

    def __addSlideToPossibleMoves(self, poz : int, dir):
        move = Directions.directions[dir[0]][dir[1]]
        basePoz = copy.copy(poz)
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            if self.state[poz] != 0:
                return
            self.__possibleMoves.append([basePoz, poz])


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
        self.__checks = 0
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

    def getDangerMap(self):
        for i in range(0, 8):
            print(self.__dangerMap[i * 8: (i+1) * 8])

    def __dangerMapHandleSliding(self, poz, dir):
        move = Directions.directions[dir[0]][dir[1]]
        pinnedPiece = -1
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            if self.withMe(poz):
                if pinnedPiece > -1:
                    if abs(self.state[poz]) == Pieces.KING:
                        self.__handlePin(pinnedPiece, dir)
                    return
                if abs(self.state[poz]) == Pieces.KING:
                    self.__handleCheck(poz, [2 - dir[0], 2 - dir[1]])
                    return
                pinnedPiece = poz
            if pinnedPiece > -1:
                continue
            if self.__dangerMap[poz] == 0:
                self.__dangerMap[poz] = 1
            if self.withEnemey(poz):
                return


    def __handleCheck(self, poz, dir):
        self.__checks += 1
        move = Directions.directions[dir[0]][dir[1]]
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            if self.state[poz] != 0:
                return
            self.__dangerMap[poz] = 2

    def __handlePin(self, poz, dir): #this function shouldn't be called to many times, so its fine to be kinda inofficient
        possibleSlides = []
        match abs(self.state[poz]):
            case Pieces.ROOK:
                if abs(dir[0] - 1) + abs(dir[1] - 1) == 1:
                    possibleSlides = [dir, [2 - dir[0], 2 - dir[1]]]
            case Pieces.BISHOP:
                if abs(dir[0] - 1) + abs(dir[1] -1) == 2:
                    possibleSlides = [dir, [2 - dir[0], 2 - dir[1]]]
            case Pieces.QUEEN:
                possibleSlides = [dir, [2 - dir[0], 2 - dir[1]]]
            case Pieces.PAWN:
                self.__handlePinnedPawn(poz, dir) #super rare case
        for i in possibleSlides:
            self.__addSlideToPossibleMoves(poz, i)
        self.state[poz] += 10


    def __handlePinnedPawn(self, poz, dir):
        if dir[0] == 1:
            return
        if self.white and dir[0] == 0 or not self.white and dir[0] == 2:
            dir = [2 - dir[0],2 - dir[1]]
        if Inside.inside[poz][dir[0]][dir[1]]:
            self.__possibleMoves.append([poz, poz + Directions.directions[dir[0]][dir[1]]])
        # TODO: fix this shit

    def __dangerMapBishop(self, poz):
        for i in Moves.Bishop:
            self.__dangerMapHandleSliding(copy.copy(poz), i)

    def __dangerMapRook(self, poz):
        for i in Moves.Rook:
            self.__dangerMapHandleSliding(copy.copy(poz), i)

    def __dangerMapQueen(self, poz):
        self.__dangerMapBishop(poz)
        self.__dangerMapRook(poz)

    def __dangerMapKing(self, poz):
        for i in Moves.King:
            if Inside.inside[poz][i[0]][i[1]]:
                self.__dangerMap[poz + Directions.directions[i[0]][i[1]]] = 1


    def __dangerMapPawn(self, poz):
        if not self.white:
            l = Moves.WhitePawnCapture
        else:
            l = Moves.BlackPawnCapture
        for j in l:
            if Inside.inside[poz][j[0]][j[1]]:
                self.__dangerMap[poz + Directions.directions[j[0]][j[1]]] = 1

    def __dangerMapKnight(self, poz):
        for i in range(0, 8):
            if KnightMoves.inside[poz][i]:
                self.__dangerMap[poz + KnightMoves.directions[i]] = 1




