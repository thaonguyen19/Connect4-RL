from connect_four import Game
from state import State, Circle

from collections import defaultdict
from copy import deepcopy
import math
import pickle
import random

class MCTSAgent:
	def __init__(self, num_simulations=100):
		self.Q = defaultdict(float)
		self.N = defaultdict(int)
		self.T = set()
		self.gamma = 0.9  # discount rate
		self.reward = 1
		self.c = 1  # exploration parameter
		self.state = State()
		self.num_simulations = num_simulations
		self.name = 'MCTSAgent'

	def play_move(self):
		best_move = self.best_move(42)
		if best_move is None:
			return None
		self.state.insert_circle(best_move)
		return best_move

	def play_opponent_move(self, move):
		self.state.insert_circle(move)

	def best_move(self, depth):
		possible = self.state.possible_insertions()
		if len(possible) == 0:
			return None

		for _ in range(self.num_simulations):
			state = deepcopy(self.state)
			self.simulate(state, depth)

		# print('N (action, count)')
		# for e in [entry for entry in self.N.items() if entry[0][0] == self.state.bitPack()]:
		# 	print(e[0][1], e[1])
		# print('Q (action, value)')
		# for e in [entry for entry in self.Q.items() if entry[0][0] == self.state.bitPack()]:
		# 	print(e[0][1], e[1])

		best_action = 0 #-1
		best_value = float("-inf")
		bitpacked_state = self.state.bitPack()
		for action in possible:
			if self.Q[(bitpacked_state, action)] > best_value:
				best_action = action
				best_value = self.Q[(bitpacked_state, action)]
		
		return best_action

	def simulate(self, state, depth):
		if depth == 0:
			return 0
		bitpacked_state = state.bitPack()
		if bitpacked_state not in self.T:
			for action in state.possible_insertions():
				self.N[(bitpacked_state, action)] = 1
				self.Q[(bitpacked_state, action)] = 0
			self.T.add(bitpacked_state)
			return self.rollout(state, depth)
		next_action = 0 #-1
		max_value = float("-inf")
		for action in state.possible_insertions():
			# calculate value of action
			matching_counts = [v for k, v in self.N.items() if k[0] == bitpacked_state]
			if matching_counts == 0 or self.N[(bitpacked_state, action)] == 0:
				value = self.Q[(bitpacked_state, action)]
			else:
				value = self.Q[(bitpacked_state, action)] + \
					self.c * math.sqrt(math.log(sum(matching_counts)) / self.N[(bitpacked_state, action)])
			if value > max_value:
				max_value = value
				next_action = action
		state.insert_circle(next_action)
		q = self.gamma * self.simulate(state, depth-1)
		self.N[(bitpacked_state, next_action)] += 1
		self.Q[(bitpacked_state, next_action)] += (q - self.Q[(bitpacked_state, next_action)]) / self.N[(bitpacked_state, next_action)]
		return q

	def rollout(self, state, depth):
		if depth == 0:
			return 0
		action = self.get_naive_policy(state)
		if action is None:
			return 0  # end of game, no winner
		state.insert_circle(action)
		winner = state.check_winner()
		if winner:
			if winner == self.state.turn:
				return self.reward
			else:
				return -self.reward
		else:
			return self.gamma * self.rollout(state, depth-1)

	def get_naive_policy(self, state):
		possible = state.possible_insertions()
		if len(possible) == 0:
			return None

		# one-move horizon check to see if any move wins immediately
		for action in possible:
			state.insert_circle(action)
			winner = state.check_winner()
			state.undo_move()
			if winner:
				return action

		return random.choice(possible)