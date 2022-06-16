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

    def findKings(self):
        pass

    def inCheck(self):
        pass

    #move handling

    def makeMove(self, move):
        pass

    def reverseMove(self, move):
        pass

    #getting possbible moves

    def getPossibleMoves(self, white = True):
        pass

    def getBishopMoves(self, poz):
        pass

    def getRookMoves(self, poz):
        pass

    def getPawnMoves(self, poz):
        pass

    def getKingMoves(self, poz):
        pass

    def getQueenMoves(self, poz):
        pass

    def getEnPassantMoves(self):
        pass

    def getCastleMoves(self):
        pass

    #get moves when pinned

    def getBishopMovesPinned(self, poz, dir):
        pass

    def getRookMovesPinned(self, poz, dir):
        pass

    def getPawnMovesPinned(self, poz, dir):
        pass

    def getKingMovesPinned(self, poz, dir):
        pass

    def getQueenMovesPinned(self, poz, dir):
        pass

    def getEnPassantMovesPinned(self, dir):
        pass

    # danger map creationn

    def createDangerMap(self):
        for i in range(0,8):
            for j in range(0,8):
                if self.white and self.board[i][j] < 0 or not self.white and self.board[i][j] > 0:
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
        pass

    def dangerMapAddSquare(self, poz):
        if self.inside([poz[0] , poz[1]]):
            self.dangerMap[poz[0]][poz[1]] = max(1, self.dangerMap[poz[0]][poz[1]])
        if self.board[poz[0]][poz[1]] == Pieces.KING and self.white or self.board[poz[0]][poz[1]] == -Pieces.KING and not self.white:
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
                if self.board[poz[0]][poz[1]] == Pieces.KING and self.white or self.board[poz[0]][poz[1]] == -Pieces.KING and not self.white:
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
                if self.board[poz[0]][poz[1]] > 0 and self.white or self.board[poz[0]][poz[1]] < 0 and not self.white:
                    foundEnemyPiece = poz
                    continue
                # if we find an enemy piece
                self.dangerMap[poz[0]][poz[1]] = max(1, self.board[poz[0]][poz[1]])
                break
            else:
                if self.board[poz[0]][poz[1]] == Pieces.KING and self.white or self.board[poz[0]][
                    poz[1]] == -Pieces.KING and not self.white:
                    self.handlePinnedPiece(poz, [i, j])
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

