import src.includes.Chess.Board as Board
import  src.includes.Chess.Move as Move

import timeit

starting_position = [
    [Board.Pieces.ROOK, Board.Pieces.KNIGHT, Board.Pieces.BISHOP, Board.Pieces.KING, Board.Pieces.QUEEN, Board.Pieces.BISHOP, Board.Pieces.KNIGHT, Board.Pieces.ROOK ],
    [Board.Pieces.BISHOP, Board.Pieces.PAWN,   Board.Pieces.PAWN,   Board.Pieces.PAWN, Board.Pieces.PAWN,  Board.Pieces.PAWN,   Board.Pieces.PAWN,   Board.Pieces.PAWN],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [-Board.Pieces.PAWN, -Board.Pieces.PAWN,   -Board.Pieces.PAWN,   -Board.Pieces.PAWN, -Board.Pieces.PAWN,  -Board.Pieces.PAWN,   -Board.Pieces.PAWN,   -Board.Pieces.PAWN],
    [-Board.Pieces.ROOK, -Board.Pieces.KNIGHT, -Board.Pieces.BISHOP, -Board.Pieces.QUEEN, -Board.Pieces.KING, -Board.Pieces.BISHOP, -Board.Pieces.KNIGHT, -Board.Pieces.ROOK ]
]

def main():
    print(Board.Inside.inside)

main()