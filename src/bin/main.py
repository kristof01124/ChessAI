import random

import src.includes.Chess.Board as Board
import src.includes.Chess.Move as Move
import timeit
import cProfile
import chess
import src.includes.Tree.Tree as Tree
import tensorflow as tf
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

def train():
    reader = csv.reader(open("chessData.csv"))
    trainBoards = []
    trainEvals = []
    testBoard = Board.Board()
    for i in reader:
        if i[1][0] == '#' or i[1] == "Evaluation":
            continue
        if len(trainEvals) % 10000 == 0:
            print(len(trainEvals))
        if len(trainEvals) == 1000:
            break
        testBoard.importFen(i[0])
        if not testBoard.white:
            testBoard.reverse()
            i[1] = - float(i[1])
        trainBoards.append(testBoard.convertBoard())
        trainEvals.append(float(i[1]))
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(736)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.35),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    #model.load_weights("model")
    model.compile(optimizer='adam',
              loss='mean_squared_error',
              metrics=['MeanAbsoluteError'])
    while True:
        index = int(random.random() * (len(trainEvals) - 1000))
        model.fit(trainBoards[index:index + 100], trainEvals[index:index + 100] ,batch_size = 1,  epochs = 1000, verbose = 2)
        model.save_weights("model")

def loadModels():
    model = tf.keras.models.Sequential([
        tf.keras.layers.InputLayer(input_shape=(736)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(1, activation='linear')
    ])
    #model.load_weights("model")
    model.compile(optimizer='adam',
                  loss='mean_squared_error',
                  metrics=['MeanAbsoluteError'])
    return model

def makePrediction(board):
    return MODEL.predict([board.convertBoard()], verbose=0)


tree = Tree.Tree(func=Board.Board.testEvaluation)
tree.board().importFen("r2qkb1r/pp1bnpp1/2n4p/2ppQ3/4pN1P/2N1P3/PPPP1PP1/R1B1KB1R w Qkq - 2 10")
print(tree.traverse(5,start=True))