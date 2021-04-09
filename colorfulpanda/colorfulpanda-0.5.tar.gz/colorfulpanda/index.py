import sys
import os
sys.path.append(os.getcwd())
from colorfulpanda.mov.BlinkBlock import main as mov
from colorfulpanda.mov.PanicWhiteRed import main as mov2


if __name__ == '__main__':
	mov2("helloworld","sorry")
