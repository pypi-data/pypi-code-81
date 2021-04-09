from colorfulpanda.utils.main import Printer, Formator
from colorfulpanda.Style.Red import style0
import time

def main(_str1, _str2, col = None, row = None):
	p = Printer()
	f = Formator(col, row)
	for i in range(4):
		pic1 = p.multi_in_style(_str1, style0, f)
		p.pln(pic1)
		time.sleep(0.2)

	p.pln(p.in_fg_color(_str2, 196))