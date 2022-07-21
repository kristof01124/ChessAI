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
        self.__castling = [True, True, True, True]
        self.__castling = [False, False, False, False]
        self.__moveHistory = []
        self.white = True
        self.__checks = 0
        self.testing = [0, 0, 0, 0, 0, 0, 0]

    #public

    def makeMove(self, mv): #doesn't check for validity of move
        if mv == [26, 17]:
            i = 0
        frm = mv[0]
        to = mv[1]
        #check for castles
        if abs(self.state[frm]) == Pieces.KING and abs(frm - to) == 2:
            self.state[to] = self.state[frm]
            self.state[frm] = 0
            match to:
                case 1:
                    self.state[2] = self.state[0]
                    self.state[0] = 0
                case 6:
                    self.state[5] = self.state[7]
                    self.state[7] = 0
                case 58:
                    self.state[59] = self.state[56]
                    self.state[56] = 0
                case 62:
                    self.state[61] = self.state[63]
                    self.state[63] = 0
            self.__moveHistory.append([frm, to, 0, self.__castling])
            return
        #check en passant
        if abs(self.state[frm]) == Pieces.PAWN and abs(to - frm) % 8 != 0 and self.state[to] == 0:
            if frm % 8 > to % 8:
                capture = frm -1
            else:
                capture = to - 1
            self.__moveHistory.append([frm, to, self.state[capture], self.__castling, True])
            self.state[to] = self.state[frm]
            self.state[frm] = 0
            self.state[capture] = 0
            return
        capture = self.state[to]
        self.state[to] = self.state[frm]
        self.state[frm] = 0
        castling = self.__castling
        if abs(self.state[to]) == Pieces.KING:
            if self.white:
                castling[0] = castling[1] = False
            else:
                castling[2] = castling[3] = False
        match to:
            case 0:
                castling[0] = False
            case 7:
                castling[1] = False
            case 56:
                castling[2] = False
            case 63:
                castling[3] = False
        self.__moveHistory.append([frm, to, capture, self.__castling, self.__possibleMoves])
        self.__castling = castling

    def makeAllMoves(self, depth = 0):
        if len(self.__moveHistory) != depth:
            print("There is a big problem")
        self.testing[depth] += 1
        if depth == 4:
            return
        lastState = copy.copy(self.state)
        self.white = not self.white
        self.getAllPossibleMoves()
        pm = copy.copy(self.__possibleMoves)
        for i in pm:
            frm = self.state[i[0]]
            to = self.state[i[1]]
            self.makeMove(i)
            self.makeAllMoves(depth + 1)
            self.reverseMove()
            if lastState != self.state:
                print("yikes")
                self.state = lastState
                self.makeMove(i)
                self.reverseMove()
        self.white = not self.white

    def reverseMove(self):
        temp = self.__moveHistory[len(self.__moveHistory) - 1]
        frm = temp[0]
        to = temp[1]
        capture = temp[2]
        castling = temp[3]
        self.__moveHistory = self.__moveHistory[0:len(self.__moveHistory) - 1]
        #handle castling
        if abs(self.state[to]) == Pieces.KING and abs(frm - to) == 2:
            self.state[frm] = self.state[to]
            self.state[to] = 0
            match to:
                case 1:
                    self.state[0] = self.state[2]
                    self.state[2] = 0
                case 6:
                    self.state[7] = self.state[5]
                    self.state[5] = 0
                case 58:
                    self.state[56] = self.state[59]
                    self.state[59] = 0
                case 62:
                    self.state[63] = self.state[61]
                    self.state[61] = 0
            return
        #handle en passant
        if temp[len(temp) - 1] is True:
            if frm % 8 > to % 8:
                capture = frm - 1
            else:
                capture = frm + 1
            self.state[frm] = self.state[to]
            self.state[to] = 0
            self.state[capture] = - self.state[frm]
            return
        self.state[frm] = self.state[to]
        self.state[to] = capture
        self.__castling = castling

    # ----------------------  POSSIBLE MOVE GENERATION ------------------------------------------------------
    def getAllPossibleMoves(self):
        self.__possibleMoves.clear()
        self.__dangerMap = [0 for i in range(0, 64)]
        self.generateDangerMap() # assume to be good for now
        self.__getEnPassantMoves() # need to be before the for range, beacuse of pins
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
            if abs(self.state[i]) >= 10:
                self.state[i] /= 10
        self.__validateMoves()
        #these don't need validation
        self.__getCastleMoves()
    #private

    def __getPossibleKingMoves(self, poz):
        for j in Moves.King:
            if Inside.inside[poz][j[0]][j[1]] and self.__dangerMap[poz + Directions.directions[j[0]][j[1]]] == 0:
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

    def __addSlideToPossibleMoves(self, poz : int, dir):
        move = Directions.directions[dir[0]][dir[1]]
        basePoz = copy.copy(poz)
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            if self.withMe(poz):
                return
            self.__possibleMoves.append([basePoz, poz])

    def __getPossiblePawnMoves(self, poz):
        if self.white:
            capture = Moves.WhitePawnCapture
            advance = Moves.WhitePawnAdvance
        else:
            capture = Moves.BlackPawnCapture
            advance = Moves.BlackPawnAdvance
        #handle captures
        for i in capture:
            move = Directions.directions[i[0]][i[1]]
            if Inside.inside[poz][i[0]][i[1]] and self.withEnemey(poz + move):
                self.__possibleMoves.append([poz, poz + move])
        #handle advance
        move = Directions.directions[advance[0]][advance[1]]
        if Inside.inside[poz][advance[0]][advance[1]] and self.state[poz + move] == 0:
            self.__possibleMoves.append([poz, poz + move])
            #handle duble advance
            if Inside.inside[poz + move][advance[0]][advance[1]] and self.state[poz + 2*move] == 0 and \
                    poz < 16 and self.white or poz >= 48 and not self.white:
                self.__possibleMoves.append([poz, poz + 2*move])

    def __getCastleMoves(self):
        found = False
        if self.white:
            if self.__castling[0] == True:
                for i in range(1, 4):
                    if self.__dangerMap[i] > 0:
                        found = True
                if not found:
                    self.__possibleMoves.append([3, 1])
            found = False
            if self.__castling[1] == True:
                for i in range(3, 7):
                    if self.__dangerMap[i] > 0:
                        found = True
                if not found:
                    self.__possibleMoves.append([3, 5])
        else:
            if self.__castling[2] == True:
                for i in range(57, 61):
                    if self.__dangerMap[i] > 0:
                        found = True
                if not found:
                    self.__possibleMoves.append([60, 58])
            found = False
            if self.__castling[3] == True:
                for i in range(60, 63):
                    if self.__dangerMap[i] > 0:
                        found = True
                if not found:
                    self.__possibleMoves.append([60, 62])

    def __getEnPassantMoves(self):
        if len(self.__moveHistory) == 0:
            return
        if self.white:
            capture = -1
        else:
            capture = 1
        poz = self.__moveHistory[len(self.__moveHistory) - 1][1]
        if abs(self.state[poz]) != Pieces.PAWN or abs(poz - self.__moveHistory[len(self.__moveHistory) - 1][0]) == 8:
            return
        for j in range(0, 3, 2):
            if Inside.inside[poz][1][j] and self.withMe(poz + Directions.directions[1][j]) and abs(self.state[poz + Directions.directions[1][j]]) == Pieces.PAWN:
                self.__possibleMoves.append([poz + Directions.directions[1][j], poz + Directions.directions[1][j] + Directions.directions[1 - capture][2 - j]])

    def __validateMoves(self):
        if self.__checks == 0:
            return
        if self.__checks == 1:
            index = len(self.__possibleMoves) -1
            temp = None
            i = 0
            while i <= index:
                if self.__dangerMap[self.__possibleMoves[i][1]] != 2 and \
                        abs(self.state[self.__possibleMoves[i][0]]) != Pieces.KING:
                    self.__possibleMoves[i] = self.__possibleMoves[index]
                    index -= 1
                    i -= 1
                i += 1
            print(len(self.__possibleMoves) - index - 1)
            self.__possibleMoves = self.__possibleMoves[0:index + 1]
            return
        index = len(self.__possibleMoves) - 1
        temp = None
        i = 0
        while i <= index:
            if abs(self.state[self.__possibleMoves[i][0]]) != Pieces.KING:
                temp = copy.copy(self.__possibleMoves[i])
                self.__possibleMoves[i] = self.__possibleMoves[index]
                self.__possibleMoves[index] = temp
                index -= 1
                i -= 1
            i += 1
        self.__possibleMoves = self.__possibleMoves[0:index + 1]
        #TODO: check after moving en passant, but super fuckin rare case, and probably irrelevant

    # ----------------------  DANGER MAP GENERATION ------------------------------------------------------
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
            else:
                if self.state[i] != 0:
                    self.__dangerMap[i] = 1
        for i in range(0, 64):
            if self.withEnemey(i):
                match abs(self.state[i]):
                    case Pieces.ROOK:
                        self.__dangerMapRook(i)
                    case Pieces.BISHOP:
                        self.__dangerMapBishop(i)
                    case Pieces.QUEEN:
                        self.__dangerMapQueen(i)

    def printMoves(self):
        for i in self.__possibleMoves:
            print(i)

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

    def __handlePin(self, poz, dir): #this function shouldn't be called too many times, so its fine to be kinda inefficient
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
        self.state[poz] *= 10

    def __handlePinnedPawn(self, poz, dir):
        if dir[0] == 1:
            return
        if self.white and   dir[0] == 0 or not self.white and dir[0] == 2:
            dir = [2 - dir[0], 2 - dir[1]]
        if Inside.inside[poz][dir[0]][dir[1]] and \
                dir[1] == 1 and self.state[poz + Directions.directions[dir[0]][dir[1]]] == 0 or dir[1] != 1 and self.withEnemey(poz + Directions.directions[dir[0]][dir[1]]):
            self.__possibleMoves.append([poz, poz + Directions.directions[dir[0]][dir[1]]])
            if dir[1] == 1 and self.state[poz + Directions.directions[dir[0]][dir[1]] * 2] == 0:
                self.__possibleMoves.append([poz, poz + Directions.directions[dir[0]][dir[1]] * 2])
        #TODO: en passant

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

    # ------------------------ HELPER FUNCTIONS -----------------------------------------------------

    def getDangerMap(self):
        for i in range(0, 8):
            print(self.__dangerMap[i * 8: (i+1) * 8])

    def __findKings(self):
        pass

    def inside(self, frm, mv):
        pass

    def withMe(self, poz):
        return self.white and self.state[poz] > 0 or not self.white and self.state[poz] < 0

    def withEnemey(self, poz):
        return self.white and self.state[poz] < 0 or not self.white and self.state[poz] > 0




