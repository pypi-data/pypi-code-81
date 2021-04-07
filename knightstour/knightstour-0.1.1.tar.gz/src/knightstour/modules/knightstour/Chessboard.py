# enables returns of custom types
from __future__ import annotations

from . TourReporter import TourReporter

"""
Knightstour objects
"""
class Chessboard(object):

	def __init__(self, x_size: int, y_size: int, reporter: TourReporter):
		self._reporter = reporter
		self._x_size = x_size
		self._y_size = y_size
		self._tour_limit = -1

		self._board = []
		for i in range(self.y_size):
			self._board.append([-1]*self.x_size)

		self._possible_changes = [(2,1),\
		(1,2),\
		(-1,2),\
		(-2,1),\
		(-2, -1),\
		(-1, -2),\
		(1,-2),\
		(2,-1)\
		]

	@property
	def tour_limit(self):
		return self._tour_limit
	
	@tour_limit.setter
	def tour_limit(self, l):
		"""
		If you want to force a smaller tour
		"""
		self._tour_limit = l



	@property
	def reporter(self):
		return self._reporter
	

	@property
	def tour_length(self):
		"""
		The length of a successful tour
		"""

		if (self.tour_limit != -1):
			return self.tour_limit 

		return self.x_size * self.y_size

	@property
	def x_size(self):
		return self._x_size

	@property
	def y_size(self):
		return self._y_size
	

	@property
	def board(self):
		return self._board
	


	@property
	def possible_changes(self):
		return self._possible_changes


	
	def pop_move(self, pos:tuple(int, int)):
		"""
		Remove the last move
		"""
		self.board[pos[0]][pos[1]] = -1

	def add_move(self, pos:tuple(int, int), move_count:int):
		"""
		Add a move to the array of used moves
		"""

		self.board[pos[0]][pos[1]] = move_count
		self.reporter.increment_moves()

	def solve_board(self) -> bool:
		
		for i in range(self.x_size):
			for ii in range(self.y_size):
				pos = (i, ii)
				self.solve_tour(pos, 1)


	def solve_tour(self, start_position:tuple(int,int), move_count:int) -> bool:
		self.add_move(start_position, move_count)

		if (move_count >= self.tour_length):
			print ("!!! WE HAVE A WINNER !!!")
			self.reporter.report_tour(self.board)
			return True


		#if (move_count > 62):
		#	print("{}".format(self.board))


		#if (self.current_depth >= 15 ):
		#	print ("!!!!! Quadrant Solved !!! {}".format(self.moves))


		for i in range(len(self.possible_changes)):
			pos = self.new_position(start_position, self.possible_changes[i])
			if self.is_legal(pos):
				#print("CHECKING MOVE: depth:{}, {},{} -> {},{}".format(move_count, start_position[0],start_position[1],  pos[0], pos[1]))

				#self.add_move(pos, move_count)
				self.solve_tour(start_position=pos, move_count=move_count+1)
				self.pop_move(pos)

		return False



	def is_legal(self, position:tuple(int,int)) -> bool:
		"""
		return true if the move is open or legal
		"""

		# out of bounds
		if (position[0] < 0 \
			or position[1] < 0 \
			or position[0] >= self.x_size \
			or position[1] >= self.y_size):

			#print("NOT LEGAL:     out of bounds:{},{}".format(position[0], position[1]))
			return False



		# already used
		if self.board[position[0]][position[1]] != -1:
			#print("NOT LEGAL:     already visited position:{},{}".format(position[0], position[1]))
			return False



		return True







	def new_position(self, start:tuple(int,int), change:tuple[int,int]) -> tuple[int,int]:
		"""
		Return a new position.
		Note, this is not guaranteed to be a legal move.

		Paramteres:
			start: starting position
			change: the change to apply

		Returns:
			tuple: a new position
		"""

		pos = (start[0] + change[0], start[1] + change[1])
		return pos








