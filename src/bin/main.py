import src.includes.Chess.Board as Board
import  src.includes.Chess.Move as Move

import timeit

def main():
    board = [
        [0, 0, Board.Pieces.KING, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [- Board.Pieces.BISHOP, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, - Board.Pieces.QUEEN, 0, 0, 0, 0, 0]
    ]
    b = Board.Board(board)
    b.createDangerMap()
    for i in b.dangerMap:
        print(i)
    print(b.checks)

main()