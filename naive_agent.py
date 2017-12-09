from connect_four import Game
from state import State, Circle

import random

class NaiveAgent:
	def __init__(self):
		self.last_move = None
		self.state = State()
		self.name = 'NaiveAgent'

	def play_move(self):
		possible = self.state.possible_insertions()
		if len(possible) == 0:
			return None

		if self.last_move is None:
			return random.choice(possible)

		neighboring_moves = []
		for offset in [-1, 0, 1]:
			if self.last_move + offset in possible:
				neighboring_moves.append(self.last_move + offset)

		return random.choice(neighboring_moves)

	def play_opponent_move(self, move):
		self.state.insert_circle(move)
		self.last_move = move