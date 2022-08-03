import copy

import chess


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
        self.__checkMap = [0 for i in range(0, 64)]
        self.state = [0 for i in range(0, 64)]
        self.__castling = [True, True, True, True]
        self.__moveHistory = []
        self.white = True
        self.__checks = 0
        self.testing = [0, 0, 0, 0, 0, 0, 0]
        self.__board = chess.Board()
        self.__enPassantSquare = -1

    #public

    def makeMove(self, mv): #doesn't check for validity of move
        frm = mv[0]
        to = mv[1]
        #check for castles
        if abs(self.state[frm]) == Pieces.KING and abs(frm - to) == 2:
            self.state[to] = self.state[frm]
            self.state[frm] = 0
            cp = copy.copy(self.__castling)
            match to:
                case 1:
                    self.state[2] = self.state[0]
                    self.state[0] = 0
                    self.__castling[0] = self.__castling[1] = False
                case 5:
                    self.state[5] = self.state[7]
                    self.state[7] = 0
                    self.__castling[0] = self.__castling[1] = False
                case 57:
                    self.state[58] = self.state[56]
                    self.state[56] = 0
                    self.__castling[2] = self.__castling[3] = False
                case 61:
                    self.state[60] = self.state[63]
                    self.state[63] = 0
                    self.__castling[2] = self.__castling[3] = False
            self.__moveHistory.append([frm, to, 0, cp, copy.copy(self.__enPassantSquare), copy.copy(self.__possibleMoves)])
            return
        #check en passant
        if len(mv) == 3:
            if frm % 8 > to % 8:
                capture = frm -1
            else:
                capture = frm + 1
            self.__moveHistory.append([frm, to, self.state[capture], copy.copy(self.__castling), copy.copy(self.__enPassantSquare), copy.copy(self.__possibleMoves)], True)
            self.state[to] = self.state[frm]
            self.state[frm] = 0
            self.state[capture] = 0
            return
        capture = self.state[to]
        self.state[to] = self.state[frm]
        self.state[frm] = 0
        cp = copy.copy(self.__castling)
        if abs(self.state[to]) == Pieces.KING:
            if self.white:
                self.__castling[0] = self.__castling[1] = False
            else:
                self.__castling[2] = self.__castling[3] = False
        match frm:
            case 0:
                self.__castling[0] = False
            case 7:
                self.__castling[1] = False
            case 56:
                self.__castling[2] = False
            case 63:
                self.__castling[3] = False
        match to:
            case 0:
                self.__castling[0] = False
            case 7:
                self.__castling[1] = False
            case 56:
                self.__castling[2] = False
            case 63:
                self.__castling[3] = False
        self.__moveHistory.append([frm, to, capture, cp, copy.copy(self.__enPassantSquare), copy.copy(self.__possibleMoves)])
        if abs(self.state[to]) == Pieces.PAWN and abs(to - frm) == 16:
            self.__enPassantSquare = (to + frm) / 2
        else:
            self.__enPassantSquare = -1
        #promotion
        if abs(self.state[to]) == Pieces.PAWN and (to >= 56 or to < 8):
            self.__moveHistory[len(self.__moveHistory) - 1].append(False)
            self.state[to] = Pieces.QUEEN * self.state[to]


    def makeAllMoves(self, depth = 0):
        self.testing[depth] += 1
        if depth == 5:
            return
        lastState = copy.copy(self.state)
        self.white = not self.white
        self.getAllPossibleMoves()
        pm = copy.copy(self.__possibleMoves)
        self.__board.set_fen(self.generateFen())
        self.__board.generate_legal_moves()
        if self.__board.legal_moves.count() != len(self.__possibleMoves):
            print("Wrong number of legal moves")
            print(self.generateFen(), self.__board.legal_moves.count(), self.__board.legal_moves, len(self.__possibleMoves), self.__possibleMoves)
            self.debugPosition()
        self.getAllPossibleMoves()
        for i in pm:
            frm = self.state[i[0]]
            to = self.state[i[1]]
            self.makeMove(i)
            self.makeAllMoves(depth + 1)
            self.reverseMove()
            if lastState != self.state:
                print("Last state doesn't match reversed state!")
                self.debugPosition()
        self.white = not self.white

    def reverseMove(self):
        temp = self.__moveHistory[len(self.__moveHistory) - 1]
        frm = temp[0]
        to = temp[1]
        capture = temp[2]
        castling = temp[3]
        enPassantSquare = temp[4]
        pm = temp[5]
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
                case 57:
                    self.state[56] = self.state[58]
                    self.state[58] = 0
                case 62:
                    self.state[63] = self.state[60]
                    self.state[60] = 0
            self.__castling = castling
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
        self.__possibleMoves = pm
        self.__enPassantSquare = enPassantSquare
        if temp[len(temp) - 1] is False:
            self.state[frm] = self.state[frm] / Pieces.QUEEN


    # ----------------------  POSSIBLE MOVE GENERATION ------------------------------------------------------
    def getAllPossibleMoves(self):
        self.__possibleMoves.clear()
        self.__dangerMap = [0 for i in range(0, 64)]
        self.__checkMap = [0 for i in range(0, 64)]
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
            #if the piece is pinned, then return it to normal
            if abs(self.state[i]) >= 10:
                self.state[i] /= 10
        self.__validateMoves()
        #these don't need validation
        self.__getCastleMoves()
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

    def __addSlideToPossibleMoves(self, poz : int, dir):
        move = Directions.directions[dir[0]][dir[1]]
        basePoz = copy.copy(poz)
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            if self.withMe(poz):
                return
            self.__possibleMoves.append([basePoz, poz])
            if self.withEnemy(poz):
                return

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
            if Inside.inside[poz][i[0]][i[1]] and (self.withEnemy(poz + move) or poz + move == self.__enPassantSquare):
                self.__possibleMoves.append([poz, poz + move])
        #handle advance
        move = Directions.directions[advance[0]][advance[1]]
        if Inside.inside[poz][advance[0]][advance[1]] and self.state[poz + move] == 0:
            self.__possibleMoves.append([poz, poz + move])
            #handle duble advance
            if Inside.inside[poz + move][advance[0]][advance[1]] and self.state[poz + 2 * move] == 0 and \
                    ((poz < 16 and self.white) or (poz >= 48 and not self.white)):
                self.__possibleMoves.append([poz, poz + 2*move])

    def __getCastle(self, frm, dir, myKing):
        found = False
        to = frm - frm % 8
        if dir > 0:
            to += 7
        for i in range(frm + dir, to, dir):
            if self.__dangerMap[i] > 0 or self.state[i] != 0:
                found = True
        if self.__dangerMap[frm] > 0:
            found = True
        if not found:
            self.__possibleMoves.append([frm, frm + 2 * dir])

    def __getCastleMoves(self):
        found = False
        if self.white:
            if self.__castling[0] == True: #white King side
                self.__getCastle(3, -1, Pieces.KING)
            if self.__castling[1] == True: #white Queen side
                self.__getCastle(3, 1, Pieces.KING)
        else:
            if self.__castling[2] == True: #black king side
                self.__getCastle(59, -1, - Pieces.KING)
            if self.__castling[3] == True: #black queen side
                self.__getCastle(59, 1, - Pieces.KING)

    def __handleEnPassantCheck(self, frm, to):
        if to % 8 > frm % 8:
            to = frm + 1
        else:
            to = copy.copy(frm)
            frm -= 1
        left = None
        right = None
        for i in range(frm - 1, frm - frm % 8 - 1, -1):
            if self.state[i] > 0:
                left = i
                break
        for i in range(to + 1, to - to % 8 + 8):
            if self.state[i] > 0:
                right = i
                break
        if right is None or left is None:
            return
        if self.withEnemy(right):
            temp = copy.copy(right)
            right = left
            left = temp
        if self.withMe(right) and abs(self.state[right]) == Pieces.KING and self.withEnemy(left) and (abs(self.state[left]) == Pieces.ROOK or abs(self.state[left]) == Pieces.QUEEN):
            self.__possibleMoves[0] = self.__possibleMoves[len(self.__possibleMoves) - 1]
            self.__possibleMoves = self.__possibleMoves[0:len(self.__possibleMoves) - 1]


    def __validateMoves(self):
        if len(self.__possibleMoves[0]) == 3:
            self.__handleEnPassantCheck(self.__possibleMoves[0][0], self.__possibleMoves[0][1])
        if self.__checks == 1:
            index = len(self.__possibleMoves) -1
            temp = None
            i = 0
            while i <= index:
                if self.__checkMap[self.__possibleMoves[i][1]] != 2 and \
                        abs(self.state[self.__possibleMoves[i][0]]) != Pieces.KING and \
                        (len(self.__possibleMoves[i]) == 2 or self.__checkMap[self.__possibleMoves[i][0] + (self.__possibleMoves[i][1] % 8 - self.__possibleMoves[i][0] % 8)] != 2) :
                    self.__possibleMoves[i] = self.__possibleMoves[index]
                    index -= 1
                    i -= 1
                i += 1
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


    # ----------------------  DANGER MAP GENERATION ------------------------------------------------------
    def generateDangerMap(self):
        self.__checks = 0
        for i in self.__dangerMap:
            i = 0
        for i in range(0, 64):
            if self.withEnemy(i):
                match abs(self.state[i]):
                    case Pieces.KING:
                        self.__dangerMapKing(i)
                    case Pieces.KNIGHT:
                        self.__dangerMapKnight(i)
                    case Pieces.PAWN:
                        self.__dangerMapPawn(i)
        for i in range(0, 64):
            if self.withEnemy(i):
                match abs(self.state[i]):
                    case Pieces.ROOK:
                        self.__dangerMapRook(i)
                    case Pieces.BISHOP:
                        self.__dangerMapBishop(i)
                    case Pieces.QUEEN:
                        self.__dangerMapQueen(i)

    def printMoves(self):
        print("The number of possible moves:", len(self.__possibleMoves))
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
                if pinnedPiece != poz and self.state[poz] != 0:
                    return
                continue
            if self.__dangerMap[poz] == 0:
                self.__dangerMap[poz] = 1
            if self.withEnemy(poz):
                return

    def __handleCheck(self, poz, dir):
        self.__checks += 1
        basepoz = poz
        move = Directions.directions[dir[0]][dir[1]]
        while Inside.inside[poz][dir[0]][dir[1]]:
            poz += move
            self.__checkMap[poz] = 2
            if self.state[poz] != 0:
                break
        move = Directions.directions[2 - dir[0]][2 - dir[1]]
        poz = basepoz
        self.__dangerMap[poz] = 1
        while Inside.inside[poz][2 - dir[0]][2 - dir[1]]:
            poz += move
            self.__dangerMap[poz] = 1
            if self.state[poz] != 0:
                return

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
                (dir[1] == 1 and self.state[poz + Directions.directions[dir[0]][dir[1]]] == 0 or dir[1] != 1 and (self.withEnemy(poz + Directions.directions[dir[0]][dir[1]]) or poz + Directions.directions[dir[0]][dir[1]] == self.__enPassantSquare)):
            self.__possibleMoves.append([poz, poz + Directions.directions[dir[0]][dir[1]]])
            if dir[1] == 1 and self.state[poz + Directions.directions[dir[0]][dir[1]] * 2] == 0 and ((poz < 16 and self.white) or (poz >= 48 and not self.white)):
                self.__possibleMoves.append([poz, poz + Directions.directions[dir[0]][dir[1]] * 2])
            return

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
                if abs(self.state[poz + Directions.directions[j[0]][j[1]]]) == Pieces.KING and self.withMe(poz + Directions.directions[j[0]][j[1]]):
                    self.__checks += 1
                    self.__checkMap[poz] = 2

    def __dangerMapKnight(self, poz):
        for i in range(0, 8):
            if KnightMoves.inside[poz][i]:
                self.__dangerMap[poz + KnightMoves.directions[i]] = 1
                if abs(self.state[poz + KnightMoves.directions[i]]) == Pieces.KING and self.withMe(poz + KnightMoves.directions[i]):
                    self.__checks += 1
                    self.__checkMap[poz] = 2

    # ------------------------ HELPER FUNCTIONS -----------------------------------------------------
    def debugPosition(self):
        print("DANGER MAP_______________________________")
        for i in range(0,64,8):
            print(self.__dangerMap[i:i+8])
        print("CHECK MAP_______________________________")
        for i in range(0, 64, 8):
            print(self.__checkMap[i:i + 8])
        print("STATE_______________________________")
        for i in range(0,64,8):
            print(self.state[i:i+8])
        print("_____________________________________________")
        print(len(self.__possibleMoves))
        print(self.__possibleMoves)
        for i in self.__moveHistory:
            print(i)

    def printState(self):
        for i in range(0, 64, 8):
            print(self.state[i:i + 8])

    def importFen(self, fen : str):
        index = 63
        self.state = [0 for i in range(0, 64)]
        for i in fen:
            piece = 0
            change = 1
            match i.lower():
                case 'p':
                    piece = Pieces.PAWN
                case 'r':
                    piece = Pieces.ROOK
                case 'b':
                    piece = Pieces.BISHOP
                case 'n':
                    piece = Pieces.KNIGHT
                case 'k':
                    piece = Pieces.KING
                case 'q':
                    piece = Pieces.QUEEN
                case '/':
                    index -= index % 8
                    index -= 1
                    continue
                case _:
                    change = ord(i) - ord('0')
            if i.lower() == i:
                piece *= -1
            self.state[index] = piece
            index -=  change
            if index % 8 == 7:
                index += 1

    def generateFen(self):
        output = ""
        index = 0
        gap = 0
        for i in reversed(self.state):
            car = None
            match abs(i):
                case Pieces.PAWN:
                    car = 'p'
                case Pieces.ROOK:
                    car = 'r'
                case Pieces.KNIGHT:
                    car = 'n'
                case Pieces.BISHOP:
                    car = 'b'
                case Pieces.KING:
                    car = 'k'
                case Pieces.QUEEN:
                    car = 'q'
                case 0:
                    gap += 1
            if i > 0:
                car = car.upper()
            if car is not None:
                if gap > 0:
                    output += str(gap)
                gap = 0
                output += car
            index += 1
            if index % 8 == 0:
                if gap > 0:
                    output += str(gap)
                    gap = 0
                output += '/'
        output = output[0:len(output) -1]
        output += " "
        if self.white:
            output += "w "
        else:
            output += "b "
        if self.__castling[0]:
            output += "K"
        if self.__castling[1]:
            output += "Q"
        if self.__castling[2]:
            output += "k"
        if self.__castling[3]:
            output += "q"
        if output[len(output) - 1] == ' ':
            output += "-"
        output += " "
        if len(self.__moveHistory) > 0:
            temp = self.__moveHistory[len(self.__moveHistory) - 1]
            if abs(temp[0] - temp[1]) == 16 and abs(self.state[temp[1]]) == Pieces.PAWN:
                output += self.generateSquareName((temp[0] + temp[1]) / 2)
            else:
                output += "-"
        else:
            output += "-"
        output += " 0 2"
        return output

    def generateSquareName(self, poz):
        match int(7 - poz%8):
            case 0:
                out = "a"
            case 1:
                out = "b"
            case 2:
                out = "c"
            case 3:
                out = "d"
            case 4:
                out = "e"
            case 5:
                out = "f"
            case 6:
                out = "g"
            case 7:
                out = "h"
        out += str(int(poz / 8) + 1)
        return out

    def getDangerMap(self):
        for i in range(0, 8):
            print(self.__dangerMap[i * 8: (i+1) * 8])

    def __findKings(self):
        pass

    def inside(self, frm, mv):
        pass

    def withMe(self, poz):
        return self.white and self.state[poz] > 0 or not self.white and self.state[poz] < 0

    def withEnemy(self, poz):
        return self.white and self.state[poz] < 0 or not self.white and self.state[poz] > 0
