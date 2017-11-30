from connect_four import Game
from state import State, Circle
from collections import defaultdict

def evaluate(state): 
	"""
	Rule: (YELLOW for the main player, RED for opponent)
	- for each column of consecutive balls (at least 2 and not blocked), the score increases by 5*sign*number of balls in col
	- for each row: count number of empty/ same color balls in the row, score increases by number of ball (at least 4) * (row_ind+1),
	to prefer lower rows
	- for each diagonal, count number of empty/same color balls in the diagonal, score increases by number of ball (at least 4)
	"""
	signs = {Circle.RED: -1, Circle.YELLOW: +1}
	return score_cols(state, signs) + score_rows(state, signs) + score_diagonals(state, signs)

def score_cols(state, signs):
	score = 0
	for c in range(7):
		col_values = state.get_column(c)[::-1]
		if col_values[-1] != Circle.EMPTY or col_values[0] == Circle.EMPTY: #if totally full or empty
			continue
		last_color_pos = col_values.index(Circle.EMPTY) - 1
		last_color = col_values[last_color_pos]
		count = 1
		for i in range(last_color_pos-1, -1, -1):
			if col_values[i] != last_color:
				break
			else:
				count += 1
		if count >= 2:
			score += 3 * signs[last_color] * count
	return score

def score_rows(state, signs):
	score = 0
	for r in range(6):
		row_values = state.get_row(r)
		first_color = None
		for i in range(7):
			if row_values[i] != Circle.EMPTY:
				color = row_values[i]
				back_i, forward_i = i-1, i+1
				count = 1
				while back_i>=0 and (row_values[back_i] == color or row_values[back_i] == Circle.EMPTY):
					count += 1
					back_i -= 1
				while forward_i <= 6 and (row_values[forward_i] == color or row_values[forward_i] == Circle.EMPTY):
					count += 1
					forward_i += 1
				if count >= 4:
					score += signs[color] * (r+1) * count
	return score

def score_diagonals(state, signs):
	score = 0
	def get_diagonal(start_coords, right):
		c, r = start_coords
		values = []
		if right:
			while r >= 0 and c <= 6:
				values.append(state.get_value(r, c))
				r -= 1
				c += 1
		else:
			while r >= 0 and c >= 0:
				values.append(state.get_value(r, c))
				r -= 1
				c -= 1
		return values

	def score_fn(diagonal_values, start_coords):
		for i in range(len(diagonal_values)):
			if diagonal_values[i] != Circle.EMPTY:
				color = diagonal_values[i]
				back_i, forward_i = i-1, i+1
				count = 1
				count_same_color = 1
				while back_i>=0 and (diagonal_values[back_i] == color or diagonal_values[back_i] == Circle.EMPTY):
					count += 1
					if diagonal_values[back_i] == color:
						count_same_color += 1
					back_i -= 1
				while forward_i < len(diagonal_values) and (diagonal_values[forward_i] == color or diagonal_values[forward_i] == Circle.EMPTY):
					count += 1
					if diagonal_values[forward_i] == color:
						count_same_color += 1
					forward_i += 1
				if count >= 4:	
					return signs[color] * count_same_color				
					break
		return 0

	for start_coords in [(0,0), (1,0), (2,0), (3,0)]: #(c, r)
		diagonal_values = get_diagonal(start_coords, True)
		score += score_fn(diagonal_values, start_coords)
	for start_coords in [(3,0), (4,0), (5,0), (6,0)]: #(c, r)
		diagonal_values = get_diagonal(start_coords, False)
		score += score_fn(diagonal_values, start_coords)
	return score

class MinimaxAgent:
	def __init__(self):
		self.Q = defaultdict(float)
		self.gamma = 0.9  # discount rate
		self.reward = 1
		self.c = 1  # exploration parameter
		self.state = State()

	def play_move(self):
		best_move = self.best_move(2) #get the action for maxAgent
		self.state.insert_circle(best_move)
		return best_move

	def play_opponent_move(self, move):
		self.state.insert_circle(move)

	def best_move(self, depth):
		bestVal, bestAction = self.minimax(True, depth)
		return bestAction

	def minimax(self, maxAgent, depth):
		#return the score based on whether we are playing with maxAgent or minAgent
		possible = self.state.possible_insertions()
		if len(possible) == 0: #draw
			return 0, None
		winner = self.state.check_winner()
		if winner == Circle.RED:
			return float('inf'), None
		elif winner == Circle.YELLOW:
			return float('-inf'), None
		if depth==0:
			return evaluate(self.state), None

		bestAction = None
		if maxAgent:
			bestVal = float('-inf')
			for action in possible:
				self.state.insert_circle(action)
				value, _ = self.minimax(False, depth)
				self.state.undo_move()
				if value >= bestVal:
					bestVal = value
					bestAction = action
		else:
			bestVal = float('inf')
			for action in possible:
				self.state.insert_circle(action)
				value = self.minimax(True, depth-1)
				self.state.undo_move()
				if value <= bestVal:
					bestVal = value
					bestAction = action				
		return bestVal, bestAction


			


