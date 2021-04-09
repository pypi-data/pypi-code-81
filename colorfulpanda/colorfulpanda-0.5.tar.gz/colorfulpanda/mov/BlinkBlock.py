from colorfulpanda.utils.main import Printer, Formator
from colorfulpanda.Style.Red import style4
import time

ONE_F = '''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
'''

SEC_F = '''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓                                   ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
'''

TRI_F = '''
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
▓▓    {}     ▓▓▓
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓
'''

def main(_str, col = None, row = None):
	p = Printer()
	f = Formator(col, row)
	for i in range(4):
		f.screen.clear_screen()
		pic1 = p.multi_in_style(SEC_F, style4, f)
		p.pln(pic1)
		time.sleep(0.3)
		f.screen.clear_screen()
		pic1 = p.multi_in_style(ONE_F, style4, f)
		p.pln(pic1)
		time.sleep(0.3)
	for i in range(2):
		f.screen.clear_screen()
		pic1 = p.multi_in_style(TRI_F.format(_str), style4, f)
		p.pln(pic1)
		time.sleep(0.3)
		f.screen.clear_screen()
		pic1 = p.multi_in_style(SEC_F.format(_str), style4, f)
		p.pln(pic1)
		time.sleep(0.3)
	f.screen.clear_screen()
	pic1 = p.multi_in_style(TRI_F.format(_str), style4, f)
	p.pln(pic1)
	time.sleep(0.3)

