import copy

import src.includes.Chess.Board as Board

INF = 10000

class Tree:
    def __init__(self, func = None):
        self.__board = Board.Board()
        self.number = 0
        if func is None:
            self.evaluate = self.baseFunction
        else:
            self.evaluate = func



    def baseFunction(self, *args):
        return 1

    def traverse(self, depth=0, alpha=-INF, beta=INF, start = False):
        if depth == 0:
            return self.evaluate(self.__board)
        self.__board.getAllPossibleMoves()
        #TODO: check for checkmate and draw
        for i in copy.copy(self.__board.possibleMoves()):
            self.__board.makeMove(i)
            val = self.traverse(depth - 1, copy.copy(alpha), copy.copy(beta))
            self.__board.reverseMove()
            if self.__board.white:
                if alpha < val:
                    alpha = val
                    if start:
                        bestMove = i
                if beta <= alpha:
                    break
            else:
                if beta > val:
                    beta = val
                    if start:
                        bestMove = i
                if beta <= alpha:
                    break
        if not start:
            if self.__board.white:
                return alpha
            return beta
        else:
            if self.__board.white:
                return [bestMove, alpha]
            return [bestMove, beta]



    def board(self):
        return self.__board