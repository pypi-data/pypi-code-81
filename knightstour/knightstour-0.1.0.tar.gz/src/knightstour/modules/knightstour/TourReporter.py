# enables returns of custom types
from __future__ import annotations

"""
Object to collect and report on all the knightstours.
"""
class TourReporter(object):

	def __init__(self, logging=True):
		self._tours_count = 0
		self._moves = 0
		self._logging = logging

		if self.logging:
			self._output = open("/ext/output_data/tours.log", "w+", 1)

	@property
	def logging(self):
		return self._logging
	

	@property
	def tours_count(self):
		"""
		Returns:
			count (int): how many tours have been reported
		"""

		return self._tours_count
	

	@property
	def moves(self):
		"""
		Each time a move is cheked, increment this count.

		Returns:
			move (int): the number of permutations.
		"""

		return self._moves
	
	def increment_moves(self):
		"""
		Increment the move count.
		"""

		self._moves = self.moves + 1

		if ((self.moves % 10000) == 0):
			print("=== Have checked another 10,000 moves: {}".format(self.moves))

		#	if (self.logging):
		#		self._output.write("=== Have checked another 10,000 moves: {}\n".format(self.moves))


	def report_tour(self, newTour: [int][int]):
		"""
		Report a new tour that has been found.

		Parameters:
			newTour: a list of tuples for each move in the tour.

		"""
		self._tours_count = self._tours_count + 1


		print("Reporting tour: {}".format(self._tours_count))

		if self.logging:
			self._output.write("Knights tour: {0}\n".format(self._tours_count))
			self._output.write("--------\n")

			for row in newTour:
				self._output.write("    {0}\n".format(row[0:]))
			self._output.write("\n")

