import pygame as pg
import sys
import game

class tictactoe:
    # sizes of interface variables
    screen_width = 600
    screen_height = 600
    line_width = 15
    square_size = 200
    circle_radius = 60
    circle_width = 15
    cross_width =25
    space = 55

    # colors of the interface variables in rgb form
    backgroud_color = (28, 170, 156)
    line_color = (0, 0, 0)
    circle_color = (239, 231, 200)
    cross_color = (66, 66, 66)

    def __init__(self, p1, p2):
        self.screen = pg.display.set_mode(( self.screen_width, self.screen_height ))
        self.board = game.Board(p1, p2)

    def mark_board(self, row, col):
        self.board.board[row][col] = self.board.playerTurn 
        self.draw_figure(row, col)
        self.board.playerTurn = 1 if self.board.playerTurn == -1 else -1
        self.board.curr_player = self.board.player1 if self.board.curr_player == self.board.player2 else self.board.player2

    def restart(self):
        self.screen.fill(self.backgroud_color)
        self.draw_boardlines()
        self.board.reset()

    def getXYPosition(self, event):
        x_coord = event.pos[0] # x coordinate
        y_coord = event.pos[1] # y coordinate
        clicked_col = int(x_coord // self.square_size)
        clicked_row = int(y_coord // self.square_size)
        return (clicked_row, clicked_col)
    

    def draw_boardlines(self):
        # horizontal lines
        pg.draw.line(self.screen, self.line_color, (0, 200), (600, 200), self.line_width)
        pg.draw.line(self.screen, self.line_color, (0, 400), (600, 400), self.line_width)
        # vertical lines
        pg.draw.line(self.screen, self.line_color, (200, 0), (200, 600), self.line_width)
        pg.draw.line(self.screen, self.line_color, (400, 0), (400, 600), self.line_width)

    def draw_cross(self, row, col):
        pg.draw.line( self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.square_size - self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.space), self.cross_width )	
        pg.draw.line( self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.square_size - self.space), self.cross_width )

    def draw_circle(self, row, col):
        pg.draw.circle( self.screen, self.circle_color, (int( col * 200 + 100 ) , int( row * 200 + 100 )), self.circle_radius, self.circle_width)

    def draw_figure(self, row, col):
        if not self.board.isAvailable(row, col):
            if self.board.playerTurn == 1:
                self.draw_circle(row,col)
            else:
                self.draw_cross(row,col)
    
    def IsGameOver(self):    
        for col in range(self.board.col):
            if self.board.board[0][col] == self.board.playerTurn and self.board.board[1][col] == self.board.playerTurn and self.board.board[2][col] == self.board.playerTurn:
                self.draw_vertical_winning_line(col)
                self.board.isEnd = True
                return

        for row in range(self.board.row):
            if self.board.board[row][0] == self.board.playerTurn and self.board.board[row][1] == self.board.playerTurn and self.board.board[row][2] == self.board.playerTurn:
                self.draw_horizontal_winning_line(row)
                self.board.isEnd = True
                return

        if self.board.board[2][0] == self.board.playerTurn and self.board.board[1][1] == self.board.playerTurn and self.board.board[0][2] == self.board.playerTurn:
            self.draw_asc_diagonal()
            self.board.isEnd = True
            return 

        if self.board.board[0][0] == self.board.playerTurn and self.board.board[1][1] == self.board.playerTurn and self.board.board[2][2] == self.board.playerTurn:
            self.draw_desc_diagonal()
            self.board.isEnd = True
            return 
        
        if self.board.isBoardFull():
            self.board.isEnd = True
            return

    def draw_vertical_winning_line(self, col):
        posX = col * self.square_size + self.square_size//2

        if self.board.playerTurn == 1:
            color = self.circle_color
        elif self.board.playerTurn == -1:
            color = self.cross_color

        pg.draw.line( self.screen, color, (posX, 15), (posX, self.screen_height - 15), self.line_width )

    def draw_horizontal_winning_line(self,row):
        posY = row * self.square_size + self.square_size//2

        if self.board.playerTurn == 1:
            color = self.circle_color
        elif self.board.playerTurn == -1:
            color = self.cross_color

        pg.draw.line( self.screen, color, (15, posY), (self.screen_width - 15, posY), self.line_width )

    def draw_asc_diagonal(self):
        if self.board.playerTurn == 1:
            color = self.circle_color
        elif self.board.playerTurn == -1:
            color = self.cross_color

        pg.draw.line( self.screen, color, (15, self.screen_height - 15), (self.screen_width - 15, 15), self.line_width )

    def draw_desc_diagonal(self):
        if self.board.playerTurn == 1:
            color = self.circle_color
        elif self.board.playerTurn == -1:
            color = self.cross_color

        pg.draw.line( self.screen, color, (15, 15), (self.screen_width - 15, self.screen_height - 15), self.line_width )

def play():
    # initialize players
    p1 = game.HumanPlayer("asdf")
    p2 = game.HumanPlayer("Wan")
    # initialzie tictactoe
    pg.init()
    new_game = tictactoe(p1,p2)
    # caption
    pg.display.set_caption("TIC TAC TOE")
    # create board
    new_game.screen.fill(new_game.backgroud_color)
    new_game.draw_boardlines() 

    while True:
        # getting events 
        for event in pg.event.get():
            # if close window exist
            if event.type == pg.QUIT:
                sys.exit()
            print(new_game.board.isEnd)
            if new_game.board.curr_player.name != "computer" and new_game.board.isEnd == False:
                if event.type == pg.MOUSEBUTTONDOWN:
                    x,y = new_game.getXYPosition(event)
                    if new_game.board.isAvailable(x,y):
                        new_game.mark_board(x,y)
                        new_game.IsGameOver()

            # elif new_game.board.curr_player.name == "computer" and new_game.board.isEnd == False:
            #     x,y = new_game.board.curr_player.move()
            #     while not new_game.board.isAvailable(x,y):
            #         x,y = new_game.board.curr_player.move()
            #     new_game.mark_board(x,y)
            #     print(new_game.board.isEnd)


            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    new_game.restart()

        pg.display.update()
        
play()