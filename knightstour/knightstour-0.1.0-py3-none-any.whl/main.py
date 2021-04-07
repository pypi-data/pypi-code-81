import sys
sys.path.append("./modules/")

from knightstour.Chessboard import Chessboard
from knightstour.TourReporter import TourReporter

tours = TourReporter()
board = Chessboard(x_size=8, y_size=8, reporter=tours)
#board.tour_limit = 64
board.solve_board()

print("moves checked: {0}".format(tours.moves))
print("we found {0} tours".format(tours.tours_count))


