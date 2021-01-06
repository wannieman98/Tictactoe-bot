import pygame as pg
import sys
import game

# class tictactoe:
#     # sizes of interface variables
#     screen_width = 600
#     screen_height = 600
#     line_width = 15
#     square_size = 200
#     circle_radius = 60
#     circle_width = 15
#     cross_width =25
#     space = 55

#     # colors of the interface variables in rgb form
#     backgroud_color = (28, 170, 156)
#     line_color = (0, 0, 0)
#     circle_color = (239, 231, 200)
#     cross_color = (66, 66, 66)

#     def __init__(self, p1, p2):
#         self.screen = pg.display.set_mode(( self.screen_width, self.screen_height ))
#         self.board = game.Board(p1, p2)


#     def draw_boardlines(self):
#         # horizontal lines
#         pg.draw.line(self.screen, self.line_color, (0, 200), (600, 200), self.line_width)
#         pg.draw.line(self.screen, self.line.color, (0, 400), (600, 400), self.line_width)
#         # vertical lines
#         pg.draw.line(self.screen, self.line.color, (200, 0), (200, 600), self.line_width)
#         pg.draw.line(self.screen, self.line.color, (400, 0), (400, 600), self.line_width)

#     def draw_cross(self, row, col):
#         pg.draw.line( self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.square_size - self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.space), self.corss_width )	
#         pg.draw.line( self.screen, self.cross_color, (col * self.square_size + self.space, row * self.square_size + self.space), (col * self.square_size + self.square_size - self.space, row * self.square_size + self.square_size - self.space), self.corss_width )

#     def draw_circle(self, row, col):
#         pg.draw.circle( self.screen, self.circle_color, (int( col * 200 + 100 ) , int( row * 200 + 100 )), self.circle_radius, self.circle_width)

#     def draw_figure(self, row, col):
#         if not self.board.isAvailable(row, col):
#             if self.board.playerTurn == 1:
#                 self.draw_circle(row,col)
#             else:
#                 self.draw_cross(row,col)

#     def mark_board(self, row, col):
#         self.board[row][col] = self.board.playerTurn 
#         draw_figure(row, col)
#         self.board.playerTurn = 1 if gameboard.playerTurn == -1 else -1
#         self.board.curr_player = p1 if gameboard.curr_player == p2 else p2
    
#     def check_winner(self):
#         pass

    # def restart(self):
    #     self.screen.fill(self.backgroud_color)
    #     self.draw_boardlines()
    #     self.board.reset()

    # def getXYPosition(self, event):
    #     x_coord = event.pos[0] # x coordinate
    #     y_coord = event.pos[1] # y coordinate
    #     clicked_col = int(x_coord // self.square_size)
    #     clicked_row = int(y_coord // self.square_size)
    #     return (clicked_row, clicked_col)


############################################################################################################


# constants
WIN_LINE_WIDTH = 15
WIDTH = 600
HEIGHT = 600
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
LINE_WIDTH = 15
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55
SQUARE_SIZE = 200

BG_COLOR = (28,170,156)
BLACK = (0,0,0)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

# player1
p1 = game.computerPlayer()

# player2 
p2 = game.HumanPlayer("Wan")

# board
gameboard = game.Board(p1, p2)



def draw_line():
    # horizontal lines
    pg.draw.line(screen, BLACK, (0,200), (600, 200), LINE_WIDTH)
    pg.draw.line(screen, BLACK, (0,400), (600, 400), LINE_WIDTH)
    # vertical lines
    pg.draw.line(screen, BLACK, (200, 0), (200, 600), LINE_WIDTH)
    pg.draw.line(screen, BLACK, (400, 0), (400, 600), LINE_WIDTH)

def draw_figure(row, col):
    if not gameboard.isAvailable(row, col):
        if gameboard.playerTurn == 1:
            pg.draw.circle( screen, CIRCLE_COLOR, (int( col * 200 + 100 ) , int( row * 200 + 100 )), CIRCLE_RADIUS, CIRCLE_WIDTH)
        else:
            pg.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
            pg.draw.line( screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_board(row, col):
    gameboard.board[row][col] = gameboard.playerTurn
    draw_figure(row, col)
    gameboard.playerTurn = 1 if gameboard.playerTurn == -1 else -1
    gameboard.curr_player = p1 if gameboard.curr_player == p2 else p2

def check_winner(player):
	# vertical win check
	for col in range(3):
		if gameboard.board[0][col] == player and gameboard.board[1][col] == player and gameboard.board[2][col] == player:
			draw_vertical_winning_line(col, player)
			return True

	# horizontal win check
	for row in range(3):
		if gameboard.board[row][0] == player and gameboard.board[row][1] == player and gameboard.board[row][2] == player:
			draw_horizontal_winning_line(row, player)
			return True

	# asc diagonal win check
	if gameboard.board[2][0] == player and gameboard.board[1][1] == player and gameboard.board[0][2] == player:
		draw_asc_diagonal(player)
		return True

	# desc diagonal win chek
	if gameboard.board[0][0] == player and gameboard.board[1][1] == player and gameboard.board[2][2] == player:
		draw_desc_diagonal(player)
		return True

	return False

def draw_vertical_winning_line(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == -1:
		color = CROSS_COLOR

	pg.draw.line( screen, color, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal_winning_line(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		color = CIRCLE_COLOR
	elif player == -1:
		color = CROSS_COLOR

	pg.draw.line( screen, color, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == -1:
		color = CROSS_COLOR

	pg.draw.line( screen, color, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		color = CIRCLE_COLOR
	elif player == -1:
		color = CROSS_COLOR

	pg.draw.line( screen, color, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )


def restart():
    screen.fill(BG_COLOR)
    draw_line()
    gameboard.reset()

pg.init()

pg.display.set_caption("TIC TAC TOE")
screen.fill(BG_COLOR)
draw_line() 


# main loop
while True:
    # getting events 
    for event in pg.event.get():
        # if close window exist
        if event.type == pg.QUIT:
            sys.exit()

        # if current player is computer, mark the board and check if game is over
        if gameboard.curr_player.name == "computer":
            x,y = gameboard.curr_player.move()
            while not gameboard.isAvailable(x,y):
                x,y = gameboard.curr_player.move()
            mark_board(x,y)
            # check winner 
            if gameboard.game_over():
            


        # else if player wait for mouse click on the board
        elif event.type == pg.MOUSEBUTTONDOWN:
            # getXYPosition(self, event)
            x_coord = event.pos[0] # x
            y_coord = event.pos[1] # y
            clicked_col = int(x_coord//SQUARE_SIZE)
            clicked_row = int(y_coord//SQUARE_SIZE)
            ######################################
            # row, col = tictactoe.getXYPosition(event)
            if gameboard.isAvailable(clicked_row, clicked_col):
                mark_board(clicked_row, clicked_col)
                # check winner



        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                restart()

    pg.display.update()