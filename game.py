import numpy as np
import random
import math

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

    def winner(self):
        for i in range(BOARD_ROWS):
            if sum(self.board[i,:]) == 3:
                self.isEnd = True
                return 1
            elif sum(self.board[i,:]) == -3:
                self.isEnd = True
                return -1
        for i in range(BOARD_COLS):
            if sum(self.board[:,i]) == 3:
                self.isEnd = True
                return 1
            elif sum(self.board[:,i]) == -3:
                self.isEnd = True
                return -1
        diag_sum1 = sum([self.board[i, i] for i in range(BOARD_COLS)])
        diag_sum2 = sum([self.board[i, BOARD_COLS - i - 1] for i in range(BOARD_COLS)])
        diag_sum = max(abs(diag_sum1), abs(diag_sum2))
        if diag_sum == 3:
            self.isEnd = True
            if diag_sum1 == 3 or diag_sum2 == 3:
                return 1
            else:
                return -1
        if self.isEnd == False and not self.isBoardFull():
            self.isEnd == True
            return 0
        else:
            return None

class HumanPlayer:
    def __init__(self, name):
        self.name = name
    
    def move(self, row, col):
        pass

class computerPlayer:
    def __init__(self):
        self.name = "computer"

    def move(self, board: Board):
        #TODO: use minimax algorithm make this ai player unbeatable
        bestScore = -math.inf
        bestMove = (0,0)
        curr_score = 0
        for x in range(board.row):
            for y in range(board.col):
                if board.isAvailable(x,y): 
                    curr_score = minimax(board, 0, False, board.playerTurn)
                    if(curr_score > bestScore):
                        bestScore = curr_score
                        bestMove = (x,y)
        return bestMove

# minimax algorithm
def minimax(board: Board, depth: int, isMaximizing: bool, turn: int) -> int:
    if board.winner() != None:
        if board.winner() == board.playerTurn:
            return 10
        elif board.winner() == 0:
            return 0 
        else:
            return -10

    if isMaximizing:
        bestScore = -math.inf
        for x in range(board.row):
            for y in range(board.col):
                if board.isAvailable(x,y):
                    board.board[x][y] = turn
                    turn = 1 if turn == -1 else -1
                    curr_score = minimax(board, depth+1, False, turn)
                    board.board[x][y] = 0
                    bestScore = max(curr_score, bestScore)
        return bestScore
    else:
        bestScore = math.inf
        for x in range(board.row):
            for y in range(board.col):
                if board.isAvailable(x,y):
                    board.board[x][y] = turn
                    turn = 1 if turn == -1 else -1
                    curr_score = minimax(board, depth+1, True, turn)
                    board.board[x][y] = 0
                    bestScore = min(curr_score, bestScore)
        return bestScore
