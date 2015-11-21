import game
from board import Board
import random
import os

moves = [Board.UP, Board.DOWN, Board.LEFT, Board.RIGHT]

def get_move():
    return random.choice(moves)


def loop():
    """
    main game loop. returns the final score.
    """
    margins = {'left': 4, 'top': 4, 'bottom': 4}

    try:
        while True:
            if game.clear_screen:
                #os.system(game.__clear)
                pass
            else:
                print("\n")
            print(game.__str__(margins=margins))
            if game.board.won() or not game.board.canMove():
                break
            m = get_move()

            game.incScore(game.board.move(m))

    except KeyboardInterrupt:
        game.saveBestScore()
        return

    game.saveBestScore()
    print('You won!' if game.board.won() else 'Game Over')
    return game.score

game = game.Game()
loop()
