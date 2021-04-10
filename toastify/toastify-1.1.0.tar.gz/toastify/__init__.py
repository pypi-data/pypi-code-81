import os
import sys

selfDir = os.path.dirname(sys.modules['toastify'].__file__)
exePath = os.path.join(selfDir, 'lib\\notify.exe')

def notify(BodyText, AppName='', AppPath='', TitleText='', ImagePath=''):

	if AppPath == '' :
		AppPath = sys.executable											# Get EXE Path

	if AppName == '' :
		AppName = AppPath[:AppPath.rfind('.')][AppPath.rfind('\\')+1:]		# Get EXE Name
	
	if ImagePath != '' :
		ImagePath = os.path.abspath(ImagePath)

	cmd = f'"{exePath}" "{AppName}" "{AppPath}" "{TitleText}" "{BodyText}" "{ImagePath}"'.replace('\\','/')

	print(cmd)
	os.system(cmd)