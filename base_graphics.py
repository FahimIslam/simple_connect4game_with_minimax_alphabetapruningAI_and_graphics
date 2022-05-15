#Basic Connect 4 game with Graphics and 2 Player Functionality
import numpy as np
import pygame
import sys
import math

pygame.init()

ROWS = 6
COLUMNS = 7

def create_board():
	board = np.zeros((ROWS,COLUMNS))
	return board

def print_board(board):
	print(np.flip(board, 0))

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def valid_location(board, col):
	return board[ROWS-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROWS):
		if board[r][col] == 0:
			return r

def check_for_win(board, piece):
	#I.Check horizontal Rows 
	for c in range(COLUMNS-3):
		for r in range(ROWS):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	#II.Check vertical Columns
	for c in range(COLUMNS):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	#III.Check positive sloped diagonals
	for c in range(COLUMNS-3):
		for r in range(ROWS-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	#IV.Check negative sloped diagonals
	for c in range(COLUMNS-3):
		for r in range(3, ROWS):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

#Initiazile Graphics
BLUE = "#1F51FF"
WHITE = "#F9F6EE"
RED = "#FF0000"
YELLOW = "#FFBF00"

SQUARESIZE = 100
width = (COLUMNS) * SQUARESIZE
height = (ROWS+1) * SQUARESIZE
size = (width, height)
RADIUS = int(SQUARESIZE/2 - 5)

myfont = pygame.font.SysFont("monospace", 70)

def draw_board(board):
	for c in range(COLUMNS):
		for r in range(ROWS):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, WHITE, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMNS):
		for r in range(ROWS):		
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == 2: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()


#Initialize the Game
board = create_board()
print_board(board)
game_over = False
turn = 0

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))
			#print(event.pos)
			#Player 1 Turn
			if turn == 0:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if check_for_win(board, 1):
						label = myfont.render("PLAYER 1 WINS!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True


			#Player 2 Turn
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if check_for_win(board, 2):
						label = myfont.render("PLAYER 2 WINS!", 1, YELLOW)
						screen.blit(label, (40,10))
						game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

			if game_over:
				pygame.time.wait(3000)