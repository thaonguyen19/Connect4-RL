from connect_four import diagonalsPos, diagonalsNeg

from enum import Enum
from itertools import groupby, chain
from math import log

class Circle(Enum):
	EMPTY = '.'
	RED = 'R'
	YELLOW = 'Y'


class State:
	def __init__(self):
		self.board = [[Circle.EMPTY] * 6 for _ in range(7)]
		self.turn = Circle.RED
		self.moves = []

	def get_value(self, r, c):
		"""
		r: from 0 to 5
		c: from 0 to 6
		"""
		return self.board[c][r]

	def get_column(self, col):
		return self.board[col]

	def get_row(self, row):
		return [self.board[col][row] for col in range(0, 7)]

	def insert_circle(self, col):
		column = self.get_column(col)

		# check if full
		if column[0] != Circle.EMPTY:
			return "error"

		insert_idx = 5-column[::-1].index(Circle.EMPTY)
		self.board[col][insert_idx] = self.turn
		self.moves.append([col, insert_idx])
		self.turn = Circle.RED if self.turn == Circle.YELLOW else Circle.YELLOW

	def undo_move(self):
		last_move = self.moves.pop()
		self.board[last_move[0]][last_move[1]] = Circle.EMPTY
		self.turn = Circle.RED if self.turn == Circle.YELLOW else Circle.YELLOW

	def possible_insertions(self):
		possible = []
		for col in range(7):
			if self.board[col][0] == Circle.EMPTY:
				possible.append(col)
		return possible

	def bitPack(self):
		"""
		First 84 bits encode value at each of 42 cells
		Last bit encodes whose turn it is
		"""
		bit = 0
		counter = 0
		n_bit_per_pos = 3
		for col in self.board:
			for circle in col:
				if circle == Circle.EMPTY:
					bit += 1 * 2**(n_bit_per_pos*counter)
				if circle == Circle.RED:
					bit += 2 * 2**(n_bit_per_pos*counter)
				if circle == Circle.YELLOW:
					bit += 4 * 2**(n_bit_per_pos*counter)
				counter += 1
		if self.turn == Circle.RED:
			bit += 1 * 2**(n_bit_per_pos*42)
		return bit

	def bitUnpack(self, bit):
		n_bit_per_pos = 3
		on_bit_pos = []
		bit_copy = bit % (2**(n_bit_per_pos*42))
		if bit_copy < bit: #largest bit = 1
			turn = Circle.RED
		else:
			turn = Circle.YELLOW
		
		while bit_copy > 0:
			p = bit_copy.bit_length()-1
			on_bit_pos.append(p)
			bit_copy -= 2**p
		all_values = [Circle.EMPTY for _ in range(42)]
		for bit_pos in on_bit_pos:
			pos = int(bit_pos/3)
			if bit_pos % 3 == 1:
				all_values[pos] = Circle.RED
			elif bit_pos % 3 == 2:
				all_values[pos] = Circle.YELLOW
		board = []
		for i in range(0, len(all_values), 6):
			board.append(all_values[i:(i+6)])
		return board, turn

	def check_winner(self):
		lines = (
			self.board, # columns
			zip(*self.board), # rows
			diagonalsPos(self.board, 7, 6), # positive diagonals
			diagonalsNeg(self.board, 7, 6) # negative diagonals
		)

		for line in chain(*lines):
			for color, group in groupby(line):
				if color != Circle.EMPTY and len(list(group)) >= 4:
					return color
