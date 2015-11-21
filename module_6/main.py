import game as myGame
from board import Board
import random
import os

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]

def get_random_move():
    return random.choice(moves)

def get_board(game):
    board = []
    for i in range(0,4):
        board.append(game.board.getCol(i))
    return board

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

def play(game):
    """
    main game loop. returns the final score.
    """
    margins = {'left': 4, 'top': 4, 'bottom': 4}

    while True:
        if not game.board.canMove():
            break
        game.incScore(game.board.move(get_random_move()))

    return get_highest_tile(game)

def play_random(n):
    results = []
    for i in range(n):
        game = myGame.Game()
        results.append(play(game))
    #print(results)
    print("Min:", min(results))
    print("Max:", max(results))
    print("Avg:", float(sum(results)/len(results)))

if __name__ == "__main__":
    play_random(100)
