import game as myGame
from board import Board
import random
import os

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]

def get_move():
    return random.choice(moves)

def get_board():
    board = []
    for i in range(0,4):
        board.append(game.board.getCol(i))
    return board

def get_highest_tile():
    board = get_board()
    highest = 0
    for i in range(0,4):
        for j in range(0,4):
            if board[j][i] > highest:
                highest = board[j][i]
    return highest

def printboard():
    board = get_board()
    for i in range(0,4):
        for j in range(0,4):
            print(board[j][i], end=" ")
        print("\n")

def play():
    """
    main game loop. returns the final score.
    """
    margins = {'left': 4, 'top': 4, 'bottom': 4}

    while True:
        if not game.board.canMove():
            break
        game.incScore(game.board.move(get_move()))

    return get_highest_tile()

if __name__ == "__main__":
    results = []
    for i in range(10000):
        game = myGame.Game()
        results.append(play())
    #print(results)
    print("Min:", min(results))
    print("Max:", max(results))
    print("Avg:", float(sum(results)/len(results)))
