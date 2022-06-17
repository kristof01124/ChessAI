class Pieces:
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Board:
    def __init__(self, board : list, white = True, castling : list = None, moveHistory : list = None):
        self.importTable(board, castling, white, moveHistory)

    #import stuff

    def importTable(self, table : list ,castling : list = None ,white = True, moveHistory : list = None):
        if castling is None:
            castling = [False, False, False, False]
        if moveHistory is None:
            moveHistory = []
        self.board = table
        self.castling = castling
        self.white = white
        self.moveHistory = moveHistory
        self.findKings()
        self.dangerMap = [[0 for i in range(0,8)] for i in range(0,8)]
        self.checks = 0
        self.possibleMoves = []

    def findKings(self):
        pass

    def inCheck(self):
        pass

    #move handling

    def makeMove(self, move):
        pass

    def reverseMove(self, move):
        pass

    #get moves when pinned
    def getBishopMovesPinned(self, poz, dir):
        if abs(poz[0]) + abs[poz[1]] != 2:
            return
        self.handleDirection(poz, dir)
        self.handleDirection(poz, [-dir[0], -dir[1]])

    def handleDirection(self, poz, dir):
        #TODO: when king is in check special case to only move to squares labeld with 2 on the dangermap
        #TODO:
        i = poz[0]
        j = poz[1]
        while True:
            i += dir[0]
            j += dir[1]
            if (not self.inside([i, j])):
                return
            if self.board[i][j] == 0:
                self.possibleMoves.append([poz, [i, j]])
                continue
            if self.withMe([i, j]):
                self.possibleMoves.append([poz, [i, j]])
            return



    def getRookMovesPinned(self, poz, dir):
        #TODO: not pinned case
        if abs(dir[0]) + abs(dir[1]) != 1:
            return
        self.handleDirection(poz, dir)
        self.handleDirection(poz, [-dir[0], -dir[1]])

    def getPawnMovesPinned(self, poz, dir):
        #TODO: not pinned case
        if self.white:
            dir = [abs(dir[0]), abs(dir[1])]
        else:
            dire = [-abs(dir[0]), -abs(dir[1])]
        match abs(dir[0]) + abs(dir[1]):
            case 1:
                if self.board[poz[0]][poz[1]] == 0:
                    self.possibleMoves.append([poz, [poz[0] + dir[0], poz[1] + dir[1]]])
                    return
            case 2:
                if not self.withMe([poz[0] + dir[0], poz[1] + dir[1]]):
                    self.possibleMoves.append([poz, [poz[0] + dir[0], poz[1] + dir[1]]])
                return

    def getKingMoves(self, poz):
        for i in range(poz[0] -1, poz[0] + 2):
            for j in range(poz[0] -1, poz[0] + 2):
                if abs(i) + abs(j) == 0:
                    continue
                if self.board[i][j] == 0 and self.dangerMap[i][j] == 0:
                    self.possibleMoves.append([poz, [i, j]])


    def getQueenMovesPinned(self, poz, dir):
        if abs(dir[0]) + abs(dir[1]) != 1:
            return
        self.handleDirection(poz, dir)
        self.handleDirection(poz, [-dir[0], -dir[1]])

    def getEnPassantMovesPinned(self, dir):
        pass

    def getKnightMovesPinned(self, dir):
        return

    # danger map creationn

    def withMe(self, poz):
        return self.board[poz[0]][poz[1]] > 0 and self.white or self.board[poz[0]][poz[1]] < 0 and not self.white

    def createDangerMap(self):
        for i in range(0,8):
            for j in range(0,8):
                if not self.withMe([i, j]):
                    match abs(self.board[i][j]):
                        case Pieces.PAWN:
                            self.dangerMapPawn([i, j])
                        case Pieces.KING:
                            self.dangerMapKing([i,j])
                        case Pieces.ROOK:
                            self.dangerMapRook([i,j])
                        case Pieces.QUEEN:
                            self.dangerMapQueen([i,j])
                        case Pieces.BISHOP:
                            self.dangerMapBishop([i,j])
                        case Pieces.KNIGHT:
                            self.dangerMapKnight([i,j])

    def inside(self, poz):
        return poz[0] < 8 and poz[0] >= 0 and poz[1] < 8 and poz[1] >= 0

    def handlePinnedPiece(self, poz, dir):
        self.board[poz[0]][poz[1]] += 10

    def dangerMapAddSquare(self, poz):
        if self.inside([poz[0] , poz[1]]):
            self.dangerMap[poz[0]][poz[1]] = max(1, self.dangerMap[poz[0]][poz[1]])
        if self.withMe(poz) and abs(self.board[poz[0]][poz[1]]) == Pieces.KING:
            self.checks += 1

    def dangerMapHandleDirection(self, poz, dir):
        i = dir[0]
        j = dir[1]
        foundEnemyPiece = None
        # increment once
        while True:
            poz[0] += i
            poz[1] += j
            if not self.inside(poz):
                break
            if foundEnemyPiece is None:
                # if there is nothing in the positions
                if self.board[poz[0]][poz[1]] == 0:
                    self.dangerMap[poz[0]][poz[1]] = 1
                    continue
                # if we found the king
                if self.withMe(poz) and abs(self.board[poz[0]][poz[1]]) == Pieces.KING:
                    temp = poz.copy()
                    self.dangerMap[poz[0]][poz[1]] = max(1, self.dangerMap[poz[0]][poz[1]])
                    poz[0] += i
                    poz[1] += j
                    while self.inside([poz[0], poz[1]]) and self.board[poz[0]][poz[1]] == 0:
                        self.dangerMap[poz[0]][poz[1]] = max(1, self.dangerMap[poz[0]][poz[1]])
                        poz[0] += i
                        poz[1] += j
                    self.checks += 1
                    poz = temp
                    poz[0] -= i
                    poz[1] -= j
                    while self.board[poz[0]][poz[1]] == 0:
                        self.dangerMap[poz[0]][poz[1]] = 2
                        poz[0] -= i
                        poz[1] -= j
                    break
                # if we find a friencly piece
                if self.withMe(poz):
                    foundEnemyPiece = poz.copy()
                    continue
                # if we find an enemy piece
                self.dangerMap[poz[0]][poz[1]] = max(1, self.board[poz[0]][poz[1]])
                break
            else:
                if self.withMe(poz) and abs(self.board[poz[0]][poz[1]]) == Pieces.KING:
                    self.handlePinnedPiece(foundEnemyPiece, [i, j])
                    break
                if self.board[poz[0]][poz[1]] != 0:
                    break

    def dangerMapBishop(self, poz):
        for i in range(-1, 2):
            for j in range(-1, 2):
                #only count diagonals
                if abs(i) + abs(j) == 2:
                    self.dangerMapHandleDirection(poz.copy(), [i, j])

    def dangerMapRook(self, poz):
        for i in range(-1, 2):
            for j in range(-1, 2):
                # only count diagonals
                if abs(i) + abs(j) == 1:
                    self.dangerMapHandleDirection(poz.copy(), [i, j])

    def dangerMapQueen(self, poz):
        for i in range(-1, 2):
            for j in range(-1, 2):
                # only count diagonals
                if abs(i) + abs(j) > 0:
                    self.dangerMapHandleDirection(poz.copy(), [i, j])

    def dangerMapKing(self, poz):
        for i in range(-1, 2):
            for j in range(-1, 2):
                # only count diagonals
                if self.inside([poz[0] + i, poz [1] + j]):
                    self.dangerMap[poz[0] + i][poz [1] + j] = max(1, self.dangerMap[poz[0] + i][poz[1] + j])

    def dangerMapPawn(self, poz):
        if self.white:
            i = -1
        else:
            i = 1
        for j in range(-1, 2, 2):
            self.dangerMapAddSquare([poz[0] + i, poz[1] + j])


    def dangerMapKnight(self, poz):
        for i in range(-2, 3, 4):
            for j in range(-1, 2, 2):
                self.dangerMapAddSquare([poz[0] + i, poz[1] + j])
                temp = i
                i = j
                j = temp
                self.dangerMapAddSquare([poz[0] + i, poz[1] + j])
                i = j

