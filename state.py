from enum import Enum

class Circle(Enum):
	EMPTY = '.'
	RED = 'R'
	YELLOW = 'Y'


class State:
	def __init__(self):
		self.board = [[Circle.EMPTY] * 6 for _ in range(7)]
		self.turn = Circle.RED

	def get_value(self, r, c):
		"""
		r: from 0 to 5
		c: from 0 to 6
		"""
		return self.board[c][r]

	def get_column(self, col):
		return self.board[col]

	def insert_circle(self, col, color):
		column = self.get_column(col)

		# check if full
		if column[0] != Circle.EMPTY:
			return "error"

		self.board[col][5-column[::-1].index(Circle.EMPTY)] = color
		self.turn = Circle.RED if color == Circle.YELLOW else Circle.YELLOW

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
		for col in self.board:
			for circle in col:
				if circle == Circle.EMPTY:
					bit += 0
				if circle == Circle.RED:
					bit += 1 * 2**(2*counter)
				if circle == Circle.YELLOW:
					bit += 2 * 2**(2*counter)
				counter += 1
		if self.turn == Circle.RED:
			bit += 1 * 2**84
		return bit

	def bitUnpack(self, bit):
		pass
