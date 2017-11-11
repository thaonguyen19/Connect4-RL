from connect_four import Game
from state import State, Circle

from collections import defaultdict
from copy import deepcopy
import pickle
import random

class Agent:
	def __init__(self):
		self.Q = defaultdict(float)
		self.gamma = 0.9  # discount rate
		self.alpha = 0.1  # learning rate
		self.lamb = 0.9  # lambda-learning rate
		self.reward = 100

	# TODO: fix
	def best_move(self, state, turn):
		"""
		Do local approximation.
		Called from connect-four.py.
		"""
		possible = state.possible_insertions()
		if len(possible) == 0:
			return None
		return random.choice(possible)

	# TODO: add negative reward for loser?
	def lambda_learn(self, trace):
		N = 1
		last = trace[-1]
		penultimate = trace[-2]
		delta = self.reward + self.gamma * self.Q[(last[0].bitPack(), last[1])] \
			- self.Q[(penultimate[0].bitPack(), penultimate[1])]
		for (state, move) in trace[::-2]:
			self.Q[(state.bitPack(), move)] += self.alpha * N * delta
			N *= self.lamb * self.gamma

	def train(self):
		g = Game()
		s = State()
		trace = []
		while True:
			move = self.best_move(s, s.turn)
			g.insert(move, s.turn.value)	
			s.insert_circle(move, s.turn)
			trace.append((deepcopy(s), move))
			if g.getWinner() is not None:
				self.lambda_learn(trace)
				g.printBoard()
				break

	def save(self, f):
		pickle.dump(self.Q, f)