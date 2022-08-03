import src.includes.Chess.Board as Board
import src.includes.Chess.Move as Move
import timeit
import cProfile
import chess

starting_position = [
    Board.Pieces.ROOK, Board.Pieces.KNIGHT, Board.Pieces.BISHOP, Board.Pieces.QUEEN, Board.Pieces.KING, Board.Pieces.BISHOP, Board.Pieces.KNIGHT, Board.Pieces.ROOK,
    Board.Pieces.PAWN , Board.Pieces.PAWN, Board.Pieces.PAWN, Board.Pieces.PAWN ,Board.Pieces.PAWN,  Board.Pieces.PAWN,   Board.Pieces.PAWN,   Board.Pieces.PAWN,
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
    board.state = starting_position
    board.importFen("rnb1kbnr/ppppp1pp/8/3KPpq1/8/7N/PPPP1PPP/RNBQ1B1R")
    #board.importFen("rnb1kbnr/pp1qPppp/8/8/8/8/PPP1PPPP/RNBQKBNR")
    board.makeAllMoves(0)
    board.debugPosition()


cProfile.run("main()")