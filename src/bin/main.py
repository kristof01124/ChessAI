import src.includes.Chess.Board as Board
import  src.includes.Chess.Move as Move
import timeit
import cProfile

starting_position = [
    Board.Pieces.ROOK, Board.Pieces.KNIGHT, Board.Pieces.BISHOP, Board.Pieces.KING, Board.Pieces.QUEEN, Board.Pieces.BISHOP, Board.Pieces.KNIGHT, Board.Pieces.ROOK,
    Board.Pieces.PAWN , Board.Pieces.PAWN,   Board.Pieces.PAWN,   Board.Pieces.PAWN, Board.Pieces.PAWN,  Board.Pieces.PAWN,   Board.Pieces.PAWN,   Board.Pieces.PAWN,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0,
    -Board.Pieces.PAWN, -Board.Pieces.PAWN,   -Board.Pieces.PAWN,   -Board.Pieces.PAWN, -Board.Pieces.PAWN,  -Board.Pieces.PAWN,   -Board.Pieces.PAWN,   -Board.Pieces.PAWN,
    -Board.Pieces.ROOK, -Board.Pieces.KNIGHT, -Board.Pieces.BISHOP, -Board.Pieces.QUEEN, -Board.Pieces.KING, -Board.Pieces.BISHOP, -Board.Pieces.KNIGHT, -Board.Pieces.ROOK
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
    board.getAllPossibleMoves()
    board.white = True
    board.getAllPossibleMoves()
    board.makeAllMoves()
    for i in range(0, 64, 8):
        print(board.state[i: i+8])
    print(board.testing)


cProfile.run("main()")