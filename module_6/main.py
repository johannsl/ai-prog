import game as myGame
from board import Board
import random
import os
import ann
import numpy
from load import normalize
from ai2048demo import welch

moves = [Board.LEFT, Board.UP, Board.RIGHT, Board.DOWN]

def setup_ai(silent=False):
    ann.run(silent)

def get_ai_move(game):
    board = get_board_weird(game)
    board = numpy.asarray(board)
    prob = ann.predict_move(board)
    #print("prob", prob)
    return moves[prob]
    
def get_ai_moves(game):
    board = get_board_weird(game)
    board = numpy.asarray(board)
    board = normalize(board)
    return ann.predict_move(board)

def get_random_move():
    return random.choice(moves)

def get_not_so_random_move():
    return random.choice(moves[:2])

def get_board(game):
    board = []
    for i in range(0,4):
        board.append(game.board.getCol(i))
    return board

def get_board_weird(game):
    board = get_board(game)
    weird = []
    for i in range(0, 4):
        for j in range(0, 4):
            weird.append(board[j][i])
    return [weird]

def get_highest_tile(game):
    board = get_board(game)
    highest = 0
    for i in range(0,4):
        for j in range(0,4):
            if board[j][i] > highest:
                highest = board[j][i]
    return highest

def printboard():
    board = get_board(game)
    for i in range(0,4):
        for j in range(0,4):
            print(board[j][i], end=" ")
        print("\n")

def play_ai(game):
    """
    main game loop. returns the final score.
    """
    margins = {'left': 4, 'top': 4, 'bottom': 4}

    #print("playing")
    while True:
        if not game.board.canMove():
            break
        board = get_board(game)
        ai_moves = get_ai_moves(game)
        while True:
            game.incScore(game.board.move(moves[numpy.argmax(ai_moves)]))
            ai_moves[numpy.argmax(ai_moves)] = 0.
            if board != get_board(game): break
    return get_highest_tile(game)

def play_random(game):
    while True:
        if not game.board.canMove():
            break
        game.incScore(game.board.move(get_random_move()))
    return get_highest_tile(game)

def run_ai(n, silent=False):
    setup_ai(silent)
    results = []
    for i in range(n):
        if not silent: print("AI player iteration", i+1, "of", n)
        game = myGame.Game()
        results.append(play_ai(game))
    return results

def run_random(n, silent=False):
    results = []
    for i in range(n):
        game = myGame.Game()
        results.append(play_random(game))
        if not silent: print("Random player iteration", i+1, "of", n)
    return results

def print_results(results):
    print("Min:", min(results))
    print("Max:", max(results))
    print("Avg:", float(sum(results)/len(results)))
    
def benchmark(n, silent=False):
    ai_result = run_ai(n, silent=True)
    random_result = run_random(n, silent=True)
    if not silent:
        ai_avg = float(sum(ai_result)/len(ai_result))
        random_avg = float(sum(random_result)/len(random_result))
        print("AI player results")
        print_results(ai_result)
        print("Random player results")
        print_results(random_result)
        print("Difference:", ai_avg - random_avg)
    print("Demo points:", welch(random_result, ai_result))

def benchmark_silent(n):
    for i in range(n):
        benchmark(50, silent=True)

if __name__ == "__main__":
    benchmark_silent(20)
