from connect_four import Game
from state import State, Circle
from mcts_agent import MCTSAgent

from collections import defaultdict
from copy import deepcopy
import pickle
import random

# Assumes that agent is yellow (ie, plays second)
class QLearningAgent:
	def __init__(self, q_file=None):
		if q_file is None:
			self.Q = defaultdict(float)
		else:
			with open(q_file, 'r') as f:
				self.Q = pickle.load(f)
		self.gamma = 0.9  # discount rate
		self.alpha = 0.1  # learning rate
		self.lamb = 0.9  # lambda-learning rate
		self.reward = 1
		self.mcts_weight = 0.1
		self.state = State()

	### Playing methods ###

	def play_move(self):
		best_move = self.best_move()
		if best_move is None:
			return None
		self.state.insert_circle(best_move)
		return best_move

	def play_opponent_move(self, move):
		self.state.insert_circle(move)

	def best_move(self):
		possible = self.state.possible_insertions()
		if len(possible) == 0:
			return None

		bitpacked_state = self.state.bitPack()
		moves_values = self.closest_moves(bitpacked_state)
		moves_values.sort(key=lambda x: x[1], reverse=True)

		# return possible move with highest q-value
		for move_value in moves_values:
			if move_value[0] in possible:
				return move_value[0]
		return random.choice(possible)

	def closest_moves(self, bitpacked_state, n_states=1):
		"""
		Performs similarity search over self.Q to find closes state
		"""
		closest = []
		max_common_bits = 0
		for state_move, q_value in self.Q.items():
			num_common_bits = bin(bitpacked_state ^ state_move[0]).count("1")
			if num_common_bits > max_common_bits:
				max_common_bits = num_common_bits
				closest = [(state_move[1], q_value)]
			if num_common_bits == max_common_bits:
				closest.append((state_move[1], q_value))
		return closest


	### Training methods ###

	# TODO: fix
	def random_move(self, state):
		"""
		Do local approximation.
		Called from connect-four.py.
		"""
		turn = state.turn
		possible = state.possible_insertions()
		if len(possible) == 0:
			return None
		return random.choice(possible)

	# TODO: add negative reward for loser?
	def lambda_learn(self, trace, agent):
		winner = agent.state.check_winner()
		if winner == Circle.YELLOW:
			sign = 1
			yellow_moves = trace[::-2]
		else:
			sign = -1
			yellow_moves = trace[:-1][::-2]

		# update based on game trace
		N = 1
		last = yellow_moves[-1]
		penultimate = yellow_moves[-2]
		delta = self.reward + self.gamma * self.Q[last] \
			- self.Q[penultimate]
		for state_move in yellow_moves:
			self.Q[state_move] += sign * self.alpha * N * delta
			N *= self.lamb * self.gamma

		# update based on Q-values from MCTS searches, with lower weight
		for state_move, value in agent.Q.items():
			self.Q[state_move] += self.mcts_weight * value

	# Idea: weight the updates from game path more than branches
	def train(self):
		red_agent = MCTSAgent(num_simulations=20)
		yellow_agent = MCTSAgent(num_simulations=20)
		trace = []
		while True:
			cur_state = yellow_agent.state.bitPack()
			turn = yellow_agent.state.turn
			if turn == Circle.RED:
				move = red_agent.play_move()
				if move is None:
					return
				yellow_agent.play_opponent_move(move)
			else:
				move = yellow_agent.play_move()
				if move is None:
					return
				red_agent.play_opponent_move(move)
			trace.append((cur_state, move))

			if yellow_agent.state.check_winner() is not None:
				self.lambda_learn(trace, yellow_agent)
				yellow_agent.state.printBoard()
				break

	def save(self, f):
		pickle.dump(self.Q, f)