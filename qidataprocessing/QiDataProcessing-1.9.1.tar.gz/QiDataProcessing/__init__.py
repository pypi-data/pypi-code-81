import os
import sys

from QiDataProcessing.QiDataController import QiDataController


sys.modules["ROOT_DIR"] = os.path.abspath(os.path.dirname(__file__))