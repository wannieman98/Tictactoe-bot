import numpy as np
import random

BOARD_ROWS = 3
BOARD_COLS = 3

class Board:
    def __init__(self, p1, p2):
        self.board = np.zeros( (BOARD_ROWS, BOARD_COLS) )
        self.player1 = p1
        self.player2 = p2
        self.curr_player = p1
        self.row = BOARD_ROWS
        self.col = BOARD_COLS
        self.playerTurn = 1
        self.isEnd = False

    def isAvailable(self, row, col):
        if self.board[row][col] == 0:
            return True
        else:
            return False

    def isBoardFull(self):
        for x in range(BOARD_ROWS):
            for y in range(BOARD_COLS):
                if self.board[x][y] == 0:
                    return False
        return True
    
    def reset(self):
        self.board = np.zeros( (self.row, self.col) )
        self.playerTurn = 1
        self.isEnd = False

class HumanPlayer:
    def __init__(self, name):
        self.name = name
    
    def move(self, row, col):
        pass

class computerPlayer:
    def __init__(self):
        self.name = "computer"

    def move(self):
        #TODO: use minimax algorithm make this self.playerTurn unbeatable
        return (random.randint(0,2), random.randint(0,2))

