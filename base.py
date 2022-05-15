#Basic Connect 4 game with 2 Player Functionality
import numpy as np

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


board = create_board()
print_board(board)
game_over = False
turn = 0


while not game_over:
    #Player 1 Input
    if turn == 0:
        col = int(input("Player 1 Turn: "))

        if valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 1)

            if check_for_win(board, 1):
                print("Player 1 has won")
                game_over = True
                
    #Player 2 Input
    else:
        col = int(input("Player 2 Turn: "))

        if valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)

            if check_for_win(board, 2):
                print("Player 2 has won")
                game_over = True

    #Print the board in loop            
    print_board(board)

    #Alternating turns between P1 & P2
    turn += 1
    turn = turn % 2

