# TO DO : fix castling through checked squares, also castle perm seems to stay 1 once it is 1
# TO DO: Add full move half move and castle permission updates
import random


class IZII:

	def __init__(self):
		self.white_pieces = "PNBRQ" # excludes king
		self.black_pieces = "pnbrq"
		self.all_white = "PKQRNBP" # includes king
		self.all_black = "pkqrnbp"
		self.black_sliders = "qrb"
		self.white_sliders = "QRB"
		self.all_pieces = "KQRBNPkqrbnp"

	# Algorithm
	def best_move(self, state, depth=2):
		# print("finding the best move")
		moves = self.get_all_moves_at_state(state)
		# print(state[5], moves)
		if state[1] == 0:
			current_score = -9999.0
		else:
			current_score = 9999.0
		move_n = -1
		turn = state[1]
		for i in range(len(moves)):
			new_state = self.move_at_state(state, moves[i])
			score = self.minimax(depth, new_state, -999, 999)
			if turn == 0:
				if score > current_score:
					move_n = i
					current_score = score
				elif score == current_score:
					if random.randint(1, 5) == 3:
						move_n = i
						current_score = score
			elif turn == 1:
				# print(score, self.sq64_to_RF(self.sq120_sq64(moves[i][0])), self.sq64_to_RF(self.sq120_sq64(moves[i][1])))
				if score < current_score:
					move_n = i
					current_score = score
				elif score == current_score:
					if random.randint(1, 5) == 3:
						move_n = i
						current_score = score
		self.print_move(moves[move_n])
		if move_n == -1:
			print("FUCKK")
		return move_n

	def minimax(self, depth, state, alpha, beta):
		# state = node.get_state()
		player_turn = state[1]

		if depth == 0:
			b_val = self.evaluate_state(state)
			# print("board value: ", b_val)
			# self.print_board(state[0])
			return b_val
		legal_moves = self.get_all_moves_at_state(state)
		# if len(legal_moves) == 0:
		# 	# print("MATE FOUND IN MINIMAX")
		# 	# self.print_board(state[0])
		# 	if player_turn == 0:
		# 		print("BLACK WINS")
		# 		return -9999
		# 	else:
		# 		print("WHOTE WINS")
		# 		return 9999

		# else:
		if player_turn == 0:
			best_value = -999
			history = []


			if len(legal_moves) == 0:
				# print("no moves for white")
				# self.print_board(state[0])
				if self.white_in_check(state[0], state[6]):
					print("real mate found for black")
					return -9999
				else:
					return 999
				# best_value = -999999
			for i in range(len(legal_moves)):

				moveset = legal_moves[i]
				history.append(self.copy_state(state))
				state = self.run_move_at_state(state, moveset)
				value = self.minimax(depth - 1, state, alpha, beta)
				state = history.pop()
				best_value = max(best_value, value)
				alpha = max(alpha, best_value)
				if beta <= alpha:
					# print("get pruned")
					break
			return best_value
		elif player_turn == 1:
			history = []
			best_value = 999
			if len(legal_moves) == 0:
				# print("no moves for black")
				# self.print_board(state[0])
				if self.black_in_check(state[0], state[7]):
					print("real mate found for white")
					return 9999
				else:
					return -999
			for i in range(len(legal_moves)):
				moveset = legal_moves[i]
				history.append(state)
				state = self.run_move_at_state(state, moveset)
				value = self.minimax(depth - 1, state, alpha, beta)
				state = history.pop()
				best_value = min(best_value, value)
				beta = min(beta, best_value)
				if beta <= alpha:
					# print("get pruned")
					break
			return best_value

	def evaluate_state(self, state):

	# print("mobility diff: ", white_move_count-black_move_count)
		count = {'K': 0, 'Q': 0, 'R': 0, 'B': 0, 'N': 0, 'P': 0, 'k': 0, 'q': 0, 'r': 0, 'b': 0, 'n': 0, 'p': 0}
		for i in state[0]:
			if i in "KQRBNPkqrbnp":
				count[i] += 1
		value = ((1000.0 * (count['K'] - count['k'])) + (9.0 * (count['Q'] - count['q'])) +
				(5.0 * (count['R'] - count['r'])) + (3.0 * (count['B'] - count['b'])) +
				(3.25 * (count['N'] - count['n'])) + (1.0 * (count['P'] - count['p'])))
				# +(.1 * (white_move_count - black_move_count)))

		# value = 0
		# white_castle = 0
		# black_castle = 0
		# if state[1] == 0 or state[1] == 1:
		# 	if state[5][0] == -1 or state[5][1] == -1:
		# 		value -= 1
		# 	if state[5][0] == 2 and state[5][1] == 2:
		# 		value += 10
		# if state[1] == 0:
		if state[5][0] == 2 or state[5][1] == 2:
			# print("white castle")
				value += 1
		elif state[5][0] == -1 or state[5][1] == -1:
				value -= 1

		if state[5][2] == 2 or state[5][3] == 2:
			# print("white castle")
				value -= 1
		elif state[5][2] == -1 or state[5][3] == -1:
				value += 1
		# if state[5][2] == 2 or state[5][3] == 2:
		# 	# print("white castle")
		# 		value -= 1000
		# elif state[5][2] == -1 or state[5][3] == -1:
		# 		value += 1000
		# print(value)
			# black_castle = -100
		# print("value pre:", value)

		# value += black_castle
		# print("value post: ", value)
		# value += 1000*(white_castle - black_castle)
		# value += 2 * (state[5][0]-state[5][2]) + 2 * (state[5][1]-state[5][3])

		return value

	def run_move_at_state(self, state, move):
		# self.save_state_to_hist()
		# print(move)
		# print(self.sq64_to_RF(self.sq120_sq64(move[0])))
		# print(self.sq64_to_RF(self.sq120_sq64(move[0][1])))
		return_state = self.move_at_state(state, move)
		return return_state

	def move_at_state(self, state, move):
		board = list(state[0])
		turn = state[1]
		en_pass_sq = state[2]
		half_move = state[3]
		full_move = state[4]
		castle_perm = list(state[5])
		white_king_sq = state[6]
		black_king_sq = state[7]
		# board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq = self.unpack_state(state)
		from_tile_n = move[0]
		to_tile_n = move[1]
		# print(to_tile_n)
		### En Passant case
		if board[from_tile_n] == 'P':
			if abs(to_tile_n-from_tile_n) == 20:
				en_pass_sq = from_tile_n - 10
			if board[to_tile_n - 10] == 'x':
				board[from_tile_n] = 'Q'
		elif board[from_tile_n] == 'p':
			if abs(to_tile_n-from_tile_n) == 20:
				en_pass_sq = from_tile_n + 10
			if board[to_tile_n + 10] == 'x':
				board[from_tile_n] = 'q'
		### King move case

		elif board[from_tile_n] == 'K':
			white_king_sq = to_tile_n
			castle_perm[0] = -1
			castle_perm[1] = -1
		elif board[from_tile_n] == 'k':
				black_king_sq = to_tile_n
				castle_perm[2] = -1
				castle_perm[3] = -1
		elif board[from_tile_n] == 'R':
			if from_tile_n == 98:  # king side
				castle_perm[0] = -1
			elif from_tile_n == 91:
				castle_perm[1] = -1
		elif board[from_tile_n] == 'r':
			if from_tile_n == 28:  # king side
				castle_perm[2] = -1
			elif from_tile_n == 21:
				castle_perm[3] = -1


		# Update Count
		# if board[to_tile_n] in self.all_pieces:
		# 	print(self.all_pieces.index(board[to_tile_n]))
			# self.count[self.all_pieces.index(board[to_tile_n])] -= 1
			# self.count[0] -= 1
		# Actually Move
		# print("moving:", board[from_tile_n])
		if from_tile_n == 0 and to_tile_n == 0:  # king side castle
			# print("I castled!")
			board[95] = "o"
			board[96] = 'R'
			board[97] = 'K'
			board[98] = 'o'
			castle_perm[0] = 2
			castle_perm[1] = 2

		elif from_tile_n == 1 and to_tile_n == 0:  # queen side castle
			# print("I castled!")
			board[91] = "o"
			board[92] = 'o'
			board[93] = 'K'
			board[94] = 'R'
			board[95] = 'o'
			castle_perm[0] = 2
			castle_perm[1] = 2
		elif from_tile_n == 1 and to_tile_n == 1:  # king side castle
			# print("I castled!")
			board[25] = "o"
			board[26] = 'r'
			board[27] = 'k'
			board[28] = 'o'
			castle_perm[2] = 2
			castle_perm[3] = 2
		elif from_tile_n == 0 and to_tile_n == 1:  # queen side castle
			# print("I castled!")
			board[21] = "o"
			board[22] = 'r'
			board[23] = 'k'
			board[24] = 'o'
			board[25] = 'o'
			castle_perm[2] = 2
			castle_perm[3] = 2

		else:
			board[to_tile_n] = board[from_tile_n]
			board[from_tile_n] = "o"

		# test if casstel legal


		# Change Turns
		if turn == 0:
			turn = 1
		else:
			turn = 0
		# print(board[to_tile_n])
		return board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq

	# Castle
	def check_wc_k(self, state): # return true if kingside castle is availible
		# check if im in check
		# check if state perm is valid
		# check if the path is clear
		castle_perm = state[5][0]
		board = state[0]
		if self.white_in_check(state[0], state[6]):
			return False
		elif castle_perm == -1:
			return False
		elif board[96] == 'o' and board[97] == 'o' and castle_perm != -1 and castle_perm != 2:
			# self.print_board(board)

			# print("wk clear")
			return True
		else:
			# print("white castle none case")
			return False

	def check_wc_q(self, state): # return true if kingside castle is availible
		# check if im in check
		# check if state perm is valid
		# check if the path is clear
		board = state[0]
		castle_perm = state[5][1]
		if self.white_in_check(state[0], state[6]):
			return False
		elif castle_perm == -1:
			return False
		elif board[92] == 'o' and board[93] == 'o' and board[94] == 'o' and castle_perm != -1 and castle_perm != 2:
			# self.print_board(board)
			# print("wq clear")
			return True
		# else:
			# print("white castle none case")
		return False

	def check_bc_k(self, state): # return true if kingside castle is availible
		# check if im in check
		# check if state perm is valid
		# check if the path is clear
		board = state[0]
		castle_perm = state[5][2]
		if self.black_in_check(state[0], state[7]):
			return False
		elif state[5][0] == -1:
			return False
		elif board[26] == 'o' and board[27] == 'o' and castle_perm != -1:
			# self.print_board(board)
			# print("bk clear")
			return True
		# else:
			# print("white castle none case")
		return False

	def check_bc_q(self, state): # return true if kingside castle is availible
		# check if im in check
		# check if state perm is valid
		# check if the path is clear
		board = state[0]
		castle_perm = state[5][3]
		if self.black_in_check(state[0], state[7]):
			return False
		elif castle_perm == -1:
			return False
		elif board[22] == 'o' and board[23] == 'o' and board[24] == 'o' and castle_perm != -1:
			# self.print_board(board)
			# print("bq clear")
			return True
		# else:
			# print("white castle none c
		return False

	# Check
	def white_in_check(self, board, tile_n):
		# self.print_board(board)
		if self.check_black_sliders(board, tile_n) is True:
			return True
		if self.check_black_knights(board, tile_n) is True:
			return True
		if self.check_black_king(board, tile_n) is True:
			return True
		if self.check_black_pawns(board, tile_n) is True:
			return True
		else:
			return False

	def black_in_check(self, board, tile_n):
		if self.check_white_sliders(board, tile_n) is True:
			# print("fucking sliders")
			return True
		if self.check_white_knights(board, tile_n) is True:
			return True
		if self.check_white_king(board, tile_n) is True:
			return True
		if self.check_white_pawns(board, tile_n) is True:
			return True
		else:

			return False

	def check_black_pawns(self, board, tile_n):
		if board[tile_n-11] == 'p':
			# print("warning black pawn")
			return True
		if board[tile_n-9] == 'p':
			# print("warning black pawn")
			return True
		return False

	def check_white_pawns(self, board, tile_n):
		if board[tile_n+11] == 'P':
			# print("warning white pawn")
			return True
		if board[tile_n+9] == 'P':
			# print("warning white pawn")

			return True
		return False

	def check_black_king(self, board, tile_n):
		directions = [11, 10, 9, 1, -11, -10, -9, -1]
		for direction in directions:
			if board[tile_n + direction] == 'k':
				return True
		return False

	def check_white_king(self, board, tile_n):
		directions = [11, 10, 9, 1, -11, -10, -9, -1]
		for direction in directions:
			if board[tile_n + direction] == 'K':
				return True
		return False

	def check_black_knights(self, board, tile_n):
		directions = [21, 19, 12, 8, -21, -19, -8, -12]
		for direction in directions:
			if board[tile_n+direction] == 'n':
				return True
		return False

	def check_white_knights(self, board, tile_n):
		directions = [21, 19, 12, 8, -21, -19, -8, -12]
		for direction in directions:
			if board[tile_n+direction] == 'N':
				return True
		return False

	def check_black_sliders(self, board, tile_n):
		slider_found = False
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			if board[i] in "qr":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			if board[i] in "qr":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			if board[i] in "qr":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break


		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			if board[i] in "qr":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_white:
				break

		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			if board[i] in "qb":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			if board[i] in "qb":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			if board[i] in "qb":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break
		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			if board[i] in "qb":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkrn":
				break
			if board[i] in self.all_white:
				break

		return slider_found

	def check_white_sliders(self, board, tile_n):
		slider_found = False
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			if board[i] in "QR":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			if board[i] in "QR":
				# print("queen rook ")
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				# print("blocked by black")
				break
		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			if board[i] in "QR":
				# print("slider at", self.sq64_to_RF(self.sq120_sq64(i)))
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			if board[i] in "QR":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "PKBN":
				break
			if board[i] in self.all_black:
				break

		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			if board[i] in "QB":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			if board[i] in "QB":
				slider_found = True
				return slider_found  # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			if board[i] in "QB":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break
		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			if board[i] in "QB":
				slider_found = True
				return slider_found # no need to check any more
			if board[i] in "pkbn":
				break
			if board[i] in self.all_black:
				break
		return slider_found

	# Get Moves
	def get_all_moves_at_state(self, state):
		# print(state)
		psuedo = self.get_pseudo_moves_beta(state)
		# print("print pseudo", psuedo, state[5])
		legal = self.get_legal_moves_beta(state, psuedo)
		# print("legal: ", legal, state[5])
		# if [0,0] in legal:
		# 	print("WHITE KIBNG CASTLE")
		# 	state[5][0] = 1
		# elif state[5][0] == 1:
		# 	state[5][0] = 0
		# print(legal)
		return legal

	def get_piece_moves(self, state, tile_n):
		board = state[0]
		en_pass_sq = state[2]
		result = []
		# print(tile_n, board[tile_n])
		if board[tile_n] == "P":
			result = self.get_white_pawn_moves(board, en_pass_sq, tile_n)
		if board[tile_n] == "p":
			result = self.get_black_pawn_moves(board, en_pass_sq, tile_n)
		if board[tile_n] == "K":
			result = self.get_white_king_moves(board, tile_n)
		if board[tile_n] == "k":
			result = self.get_black_king_moves(board, tile_n)
		if board[tile_n] == "R":
			result = self.get_white_rook_moves(board, tile_n)
		if board[tile_n] == "r":
			result = self.get_black_rook_moves(board, tile_n)
		if board[tile_n] == "B":
			result = self.get_white_bishop_moves(board, tile_n)
		if board[tile_n] == "b":
			result = self.get_black_bishop_moves(board, tile_n)
		if board[tile_n] == "N":
			result = self.get_white_knight_moves(board, tile_n)
		if board[tile_n] == "n":
			result = self.get_black_knight_moves(board, tile_n)
		if board[tile_n] == "Q":
			result = self.get_white_queen_moves(board, tile_n)
		if board[tile_n] == "q":
			result = self.get_black_queen_moves(board, tile_n)
		return result

	def get_pseudo_moves_beta(self, state):
		moves = []
		b = state[0]
		turn = state[1]
		for i in range(len(b)):
			if turn == 0:
				if b[i] in self.all_white:
					piece_moves = self.get_piece_moves(state, i)
					for k in range(len(piece_moves)):
						moves.append([i, piece_moves[k]])
					# if len(piece_moves) > 0:
					# 	moves.append([i, piece_moves])
			elif turn == 1:
				if b[i] in self.all_black:
					piece_moves = self.get_piece_moves(state, i)
					for k in range(len(piece_moves)):
						moves.append([i, piece_moves[k]])
					# if len(piece_moves) > 0:
					# 	moves.append([i, piece_moves])

		if state[1] == 0:
			# print("checking white castle")
			# self.print_board(state[0])
			if self.check_wc_k(state):  # if im not in check and i have not fucked up my castle perm add the move
				state[5][0] = 1
				# print("WK GOOOD")
				moves.append([0, 0])
			if self.check_wc_q(state):
				state[5][1] = 1
				moves.append([1, 0])
		if state[1] == 1:
			if self.check_bc_k(state):
				state[5][2] = 1
				moves.append([1, 1])
			if self.check_bc_q(state):
				state[5][3] = 1
				moves.append([0, 1])
		return moves

	def get_legal_moves_beta(self, state, pseudo_moves):
		# take move
		# check if in check
		# valid/invalid move
		# undo move
		legal_moves = []
		in_check = False
		# if state[1] == 0:
		# print("pseudo moves: ", pseudo_moves)
		for i in range(len(pseudo_moves)):
			move_set = pseudo_moves[i]
			from_sq = move_set[0]
			to_sq = move_set[1]
			# for j in range(len(to_sqs)):
			if pseudo_moves[i] == [0, 0]:
				# print("ITS wk CASTLE TIME")
				s2 = self.run_move_at_state(state, (95, 97))  # move king
				s2 = self.run_move_at_state(state, (98, 96))  # move queen
			elif pseudo_moves[i] == [1, 0]:
				# print("ITS wq CASTLE TIME")
				s2 = self.run_move_at_state(state, (95, 93))  # move king
				s2 = self.run_move_at_state(state, (91, 94))  # move queen
			elif pseudo_moves[i] == [1, 1]:
				# print("ITS bk CASTLE TIME")
				s2 = self.run_move_at_state(state, (25, 27))  # move king
				s2 = self.run_move_at_state(state, (28, 26))  # move queen
			elif pseudo_moves[i] == [0, 1]:
				# print("ITS bq CASTLE TIME")
				s2 = self.run_move_at_state(state, (25, 23))  # move king
				s2 = self.run_move_at_state(state, (21, 24))  # move queen
			else:
				s2 = self.run_move_at_state(state, (from_sq, to_sq))

			if s2[1] == 1:
				in_check = self.white_in_check(s2[0], s2[6])

			elif s2[1] == 0:
				in_check = self.black_in_check(s2[0], s2[7])
			if in_check is False:
				legal_moves.append(pseudo_moves[i])
			# else:
			# self.print_board(s2[0])
			# print("in check")
			# 	pass
			# if state[1] == 0:
			# if state[5][0] == 1
			# state[5][0] = 0
			# state[5][1] = 0
			# elif state[1] == 1:
			# 	state[5][2] = 0
			# 	state[5][3] = 0


			# if in_check is False:
			# 	legal_set.append(to_sq)
			# else:
			# print("check")
			# self.undo()
			# if len(legal_set) > 0:
			# 	legal_moves.append([from_sq, legal_set])
			# legal_set = []
		return legal_moves

	def get_black_pawn_moves(self, board, en_passant_square, tile_n):
		result = []
		# en_passant_square = self.current_state[2]
		if en_passant_square != -1:
			if tile_n == en_passant_square - 9 or tile_n == en_passant_square - 11:
				result.append(en_passant_square)
		# forward
		# initial move
		if tile_n < 40: # first row
			if board[tile_n + 10] == "o":
				result.append(tile_n + 10)
				if board[tile_n + 20] == "o":
					result.append(tile_n + 20)
		else:
			if board[tile_n + 10] == "o":
				result.append(tile_n + 10)
		###########
		# attack
		#############
		if board[tile_n + 11] in self.white_pieces:  # attack left only black pawn only
			result.append(tile_n + 11)
		if board[tile_n + 9] in self.white_pieces:  # attack right only black pawn only
			result.append(tile_n + 9)
		return result

	def get_white_pawn_moves(self, board, en_passant_square, tile_n):
		result = []
		# en_passant_square = self.current_state[2]
		# forward
		# initial move
		if en_passant_square != -1:
			if tile_n == en_passant_square + 9 or tile_n == en_passant_square + 11:
				result.append(en_passant_square)
		if tile_n > 80: # first row
			if board[tile_n - 10] == "o":
				result.append(tile_n - 10)
				if board[tile_n - 20] == "o":
					result.append(tile_n - 20)
		else:
			if board[tile_n-10] == "o":
				result.append(tile_n-10)
		###########
		# attack
		#############
		if board[tile_n - 11] in self.black_pieces:  # attack left only black pawn only
			result.append(tile_n - 11)
		if board[tile_n - 9] in self.black_pieces:  # attack right only black pawn only
			result.append(tile_n - 9)
		return result

	def get_white_king_moves(self, board, tile_n):
		result = []
		down = tile_n + 10
		up = tile_n - 10
		right = tile_n - 1
		left = tile_n + 1
		up_left = tile_n - 11
		up_right = tile_n - 9
		down_left = tile_n + 9
		down_right = tile_n + 11

		# passive moves
		if board[down] == 'o':
			result.append(down)
		if board[up] == 'o':
			result.append(up)
		if board[left] == 'o':
			result.append(left)
		if board[right] == 'o':
			result.append(right)
		if board[up_right] == 'o':
			result.append(up_right)
		if board[down_right] == 'o':
			result.append(down_right)
		if board[up_left] == 'o':
			result.append(up_left)
		if board[down_left] == 'o':
			result.append(down_left)

		# attack moves
		if board[down] in self.black_pieces:
			result.append(down)
		if board[up] in self.black_pieces:
			result.append(up)
		if board[left] in self.black_pieces:
			result.append(left)
		if board[right] in self.black_pieces:
			result.append(right)
		if board[up_right] in self.black_pieces:
			result.append(up_right)
		if board[down_right] in self.black_pieces:
			result.append(down_right)
		if board[up_left] in self.black_pieces:
			result.append(up_left)
		if board[down_left] in self.black_pieces:
			result.append(down_left)

		return result

	def get_black_king_moves(self, board, tile_n):
		result = []
		up = tile_n + 10
		down = tile_n - 10
		left = tile_n - 1
		right = tile_n + 1
		down_right = tile_n - 11
		down_left = tile_n - 9
		up_right = tile_n + 9
		up_left = tile_n + 11

		# passive moves
		if board[down] == 'o':
			result.append(down)
		if board[up] == 'o':
			result.append(up)
		if board[left] == 'o':
			result.append(left)
		if board[right] == 'o':
			result.append(right)
		if board[up_right] == 'o':
			result.append(up_right)
		if board[down_right] == 'o':
			result.append(down_right)
		if board[up_left] == 'o':
			result.append(up_left)
		if board[down_left] == 'o':
			result.append(down_left)

		# attack moves
		if board[down] in self.white_pieces:
			result.append(down)
		if board[up] in self.white_pieces:
			result.append(up)
		if board[left] in self.white_pieces:
			result.append(left)
		if board[right] in self.white_pieces:
			result.append(right)
		if board[up_right] in self.white_pieces:
			result.append(up_right)
		if board[down_right] in self.white_pieces:
			result.append(down_right)
		if board[up_left] in self.white_pieces:
			result.append(up_left)
		if board[down_left] in self.white_pieces:
			result.append(down_left)

		return result

	def get_white_rook_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		return result

	def get_black_rook_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break
		return result

	def get_white_bishop_moves(self, board, tile_n):
		result = []
		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		return result

	def get_black_bishop_moves(self, board, tile_n):
		result = []
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break

		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break
		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break
		return result

	def get_white_knight_moves(self, board, tile_n):
		result = []
		directions = [21, 19, 12, 8, -21, -19, -8, -12]
		for i in range(len(directions)):
			if board[tile_n+directions[i]] == 'o' or board[tile_n+directions[i]] in self.black_pieces:
				result.append(tile_n+directions[i])
		return result

	def get_black_knight_moves(self, board, tile_n):
		result = []
		directions = [21, 19, 12, 8, -21, -19, -8, -12]
		for i in range(len(directions)):
			if board[tile_n+directions[i]] == 'o' or board[tile_n+directions[i]] in self.white_pieces:
				result.append(tile_n+directions[i])
		return result

	def get_white_queen_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break
		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.black_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.white_pieces or board[i] == "K" or board[i] == "k":
				break

		return result

	def get_black_queen_moves(self, board, tile_n):
		result = []
		# UP
		i = tile_n
		while board[i] != 'x':
			i += 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break
		# DOWN
		i = tile_n
		while board[i] != 'x':
			i -= 10
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# LEFT
		i = tile_n
		while board[i] != 'x':
			i += 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 1
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "k" or board[i] == "K":
				break

		# DOWN LEFT
		i = tile_n
		while board[i] != 'x':
			i += 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break

		# DOWN RIGHT
		i = tile_n
		while board[i] != 'x':
			i += 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break
		# UP LEFT
		i = tile_n
		while board[i] != 'x':
			i -= 9
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break

		# UP RIGHT
		i = tile_n
		while board[i] != 'x':
			i -= 11
			# open square
			if board[i] == 'o':
				result.append(i)
			# attack
			if board[i] in self.white_pieces:
				# print("ATTACK WITH ROOK")
				result.append(i)
				break
			# self block
			if board[i] in self.black_pieces or board[i] == "K" or board[i] == "k":
				break

		return result

	def get_board(self):
		return self.current_state[0]

	# Helper Functions
	def RF_sq64(self, file, rank):
		sq = 0
		file = file.upper()
		if file == 'A':
			file = 1
		elif file == 'B':
			file = 2
		elif file == 'C':
			file = 3
		elif file == 'D':
			file = 4
		elif file == 'E':
			file = 5
		elif file == 'F':
			file = 6
		elif file == 'G':
			file = 7
		elif file == 'H':
			file = 8
		else:
			file = -1
			# print("error unkown file")
		sq = abs(rank-9)*8-8 + file
		return sq

	def sq64_to_RF(self, sq64):

		rank = 0
		if sq64 <= 8:
			rank = '8'
		elif sq64 <= 16:
			rank = '7'
		elif sq64 <= 24:
			rank = '6'
		elif sq64 <= 32:
			rank = '5'
		elif sq64 <= 40:
			rank = '4'
		elif sq64 <= 48:
			rank = '3'
		elif sq64 <= 56:
			rank = '2'
		elif sq64 <= 64:
			rank = '1'

		file = sq64 % 8
		if file == 1:
			file = 'A'
		elif file == 2:
			file = 'B'
		elif file == 3:
			file = 'C'
		elif file == 4:
			file = 'D'
		elif file == 5:
			file = 'E'
		elif file == 6:
			file = 'F'
		elif file == 7:
			file = 'G'
		elif file == 0:
			file = 'H'
		else:
			print("eror", file)
		# print(rank)
		return file, rank

	def change_turns(self):
		if self.current_state[1] == 1:
			self.current_state[1] = 0
		else:
			self.current_state[1] = 1
		# return turn

	def print_full_board(self, board):
		for i in range(0, 120):
			if i % 10 == 0:
				row = board[i:i + 10]
				row_str = ' '.join(row)
				print(i, row_str)

	def print_board(self, board):
		k = 0
		for i in range(20, 100):
			if i % 10 == 0:
				# print(board)
				# print(i)
				row = board[i + 1:i + 9]
				row_str = ' '.join(row)
				print(self.ranks[k], row_str)
				k += 1
		print('  A B C D E F G H')

	def sq120_sq64(self, sq):
		sq120 = []
		for i in range(120):
			# if i < 21:
			# 	sq120.append(-1)
			# if i > 100:
			# 	sq120.append(-1)
			# else:
			sq120.append(-1)
		skip = 0
		for i in range(20, 100):
			if i % 10 != 0 and (i -9) % 10 != 0:
				sq120[i] = i - 20 - skip
			if i % 10 == 0 and i != 20:
				skip += 2
		return sq120[sq]

	def sq64_to_sq120(self, sq):
		extra = 0
		for i in range(1, sq):
			if i % 8 == 0:
				extra += 2
		return sq + 20 + extra

	def print_move(self, move):
		print(self.sq64_to_RF(self.sq120_sq64(move[0])), self.sq64_to_RF(self.sq120_sq64(move[1])))

	def copy_state(self, state):
		board = list(state[0])
		turn = state[1]
		en_pass_sq = state[2]
		half_move = state[3]
		full_move = state[4]
		castle_perm = list(state[5])
		white_king_sq = state[6]
		black_king_sq = state[7]
		return board, turn, en_pass_sq, half_move, full_move, castle_perm, white_king_sq, black_king_sq


if __name__ == '__main__':
	engine = IzzI()
	i = 0
	current_state = init_state
	while i < 300:
		all_moves = engine.get_all_moves_at_state(current_state)
		random_int = random.randint(0, len(all_moves)-1)
		next_state = engine.run_move_at_state(current_state, all_moves[random_int])


		# engine.run_chess()
		# engine.minimaxroot(2)
		i += 1


