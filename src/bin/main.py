import random

import src.includes.Chess.Board as Board
import src.includes.Chess.Move as Move
import timeit
import cProfile
import chess
import src.includes.Tree.Tree as Tree
import csv

starting_position = [
    Board.Pieces.ROOK, Board.Pieces.KNIGHT, Board.Pieces.BISHOP, Board.Pieces.QUEEN, Board.Pieces.KING, Board.Pieces.BISHOP, Board.Pieces.KNIGHT, Board.Pieces.ROOK,
    Board.Pieces.PAWN , Board.Pieces.PAWN, Board.Pieces.PAWN, Board.Pieces.PAWN ,Board.Pieces.PAWN,  Board.Pieces.PAWN, Board.Pieces.PAWN,   Board.Pieces.PAWN,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    -Board.Pieces.PAWN, -Board.Pieces.PAWN,  - Board.Pieces.PAWN, -Board.Pieces.PAWN, -Board.Pieces.PAWN,  -Board.Pieces.PAWN,   -Board.Pieces.PAWN,   -Board.Pieces.PAWN,
    -Board.Pieces.ROOK, -Board.Pieces.KNIGHT, -Board.Pieces.BISHOP, -Board.Pieces.QUEEN,  -Board.Pieces.KING, -Board.Pieces.BISHOP, -Board.Pieces.KNIGHT, -Board.Pieces.ROOK
]

test_position = [
    0, 0, 0, 0, 0, 0, 0, 0,
    0, - Board.Pieces.KING, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, - Board.Pieces.BISHOP, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, Board.Pieces.ROOK, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
]

def main():
    board = Board.Board()
    board.importFen("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
    print(board.convertBoard())

def treeTest(n):
    tree = Tree.Tree(func=Board.Board.testEvaluation)
    tree.board().importFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    print(tree.traverse(n))
    print(tree.number)

def withoutPruning():
    board = Board.Board()
    board.importFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
    board.makeAllMoves(1)
    print(board.testing)

tree = Tree.Tree(func=Board.Board.testEvaluation)
tree.board().importFen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
print(tree.traverse(5,start=True))