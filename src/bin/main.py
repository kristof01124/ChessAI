import src.includes.Chess.Board as Board
import  src.includes.Chess.Move as Move
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
    board.getAllPossibleMoves()
    b = chess.Board()
    b.set_fen("rnbqkbnr/ppp1pppp/8/3p4/3P4/8/PPP1PPPP/RNBQKBNR w KQkq d6 0 1")
    b.generate_legal_moves()
    print(b.legal_moves.count())
    print(b.legal_moves)
    board.printMoves()
    board.makeAllMoves()
    print(board.testing)



cProfile.run("main()")