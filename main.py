#Simple Connect 4 game with Minimax Alpha-Beta Pruning AI and Graphics
import numpy as np
import pygame
import sys
import math
import random

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

#Initiazile AI
PLAYER = 0
AI = 1

PLAYER_PIECE = 1
AI_PIECE = 2

turn = random.randint(PLAYER, AI)

def evaluate_window(window, piece):
	score = 0

	opp_piece = PLAYER_PIECE

	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		score += 100
	elif window.count(piece) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(piece) == 2 and window.count(0) == 2:
		score += 2

	if window.count(opp_piece) == 3 and window.count(0) == 1:
		score -= 4

	return score

def score_position(board, piece):
	score = 0

	#Center Column Score
	center_array = [int(i) for i in list(board[:,COLUMNS//2])]
	center_count = center_array.count(piece)
	score += center_count * 3

	#Horizontal Score
	for r in range(ROWS):
		row_array = [int(i) for i in list(board[r,:])]
		for c in range(COLUMNS-3):
			window = row_array[c:c+4]
			score += evaluate_window(window, piece)

	#Vertical Score
	for c in range(COLUMNS):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROWS-3):
			window = col_array[r:r+4]
			score += evaluate_window(window, piece)

	#Posiive Diagonal Score
	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	#Negative Diagonal Score
	for r in range(ROWS-3):
		for c in range(COLUMNS-3):
			window = [board[r+3-i][c+i] for i in range(4)]
			score += evaluate_window(window, piece)

	return score

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMNS):
		if valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def is_terminal_node(board):
	return check_for_win(board, PLAYER_PIECE) or check_for_win(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):

	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)

	if depth == 0 or is_terminal:
		if is_terminal:
			if check_for_win(board, AI_PIECE):
				return (None, 100000000000000)
			elif check_for_win(board, PLAYER_PIECE):
				return (None, -10000000000000)
			#Game over, no more valid moves
			else: 
				return (None, 0)
		#If Depth is zero		
		else: 
			return (None, score_position(board, AI_PIECE))

	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, AI_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, False)[1]
			if new_score > value:
				value = new_score
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	#Minimizing player
	else: 
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			board_copy = board.copy()
			drop_piece(board_copy, row, col, PLAYER_PIECE)
			new_score = minimax(board_copy, depth-1, alpha, beta, True)[1]
			if new_score < value:
				value = new_score
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

"""
This is the depth limited minimax with alpha-beta pruning pseudocode

function alphabeta(node, depth, α, β, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if value ≥ β then
                break (* β cutoff *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if value ≤ α then
                break (* α cutoff *)
        return value
"""

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
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

#Initialize the Game
board = create_board()
print_board(board)
game_over = False

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

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, WHITE, (0,0, width, SQUARESIZE))

			#Player 1 Turn
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if check_for_win(board, PLAYER_PIECE):
						label = myfont.render("PLAYER 1 WINS!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					turn += 1
					turn = turn % 2

					print_board(board)
					draw_board(board)

	#AI Turn
	if turn == AI and not game_over:
		#Calling Minimax function on AI with initial call (origin, depth, −∞, +∞, TRUE)				
		col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)

		if valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)

			if check_for_win(board, AI_PIECE):
				label = myfont.render("PLAYER 2 WINS!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)
