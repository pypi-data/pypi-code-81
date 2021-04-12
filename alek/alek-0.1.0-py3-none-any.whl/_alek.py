'''mooses are beautiful



'''

import sys as _sys
import time as _time
import os as _os

_all_ = ['hello', 'delay_print', 'get_int', 'clear']
def hello(name):
	''' This function takes in a name, and greats the person of that name

	Args:
		name[string] the name of the person

	returns:
		a string
	'''

	string= f"Hello {name}, my name is Alek Chase"
	return string

def delay_print(s, end='', level=4):
	for c in s:
		_sys.stdout.write(c)
		_sys.stdout.flush()
		_time.sleep(0.04)
	print(end)
	''' in string, prints one character at a time is a certain interval
	Ars: 
	num[str] the name of the person
	level[int] determines the speed at which chars are printed, the higher the level,
	the slowers the chars are printed

	Returns:
		& string
	'''
	speed = 0.01*level

	for char in string:
		_sys.stdout.write(char)
		_sys.stdout.flush()
		_time.sleep(speed)
	print(end)

def clear():
	'''clears the terminal screen using the appropriate command specific to the os
	Args:
		valid(no args)
	Returns:
		valid(no returns)

		'''
	if _sys.platform.startswith('win32'):
		_os.system('cls')
	else:
		_os.system('clear')
	return 0

def get_num(prompt="Enter a number: ", start=False, finish=False, integer=False, round_up=False):
	while True:
''' Ensures the user enters a valid number internalizing the default input() function

Args:
	prompt[str]: the string that shows up as the prompt (*: * are added the end of the string)
	start[int or float]: the value that the number must be greater than (start < num)
	finish[int or float]: the value that the number must be less than (finish > num)
	interger[boolean]: true or false statement that decides of the value must be an int
	round_up[boolean]: true or false statement that decides if it will "round up" the number
	round_num[float]: float that will determine whether or not rounding is appropriate
Returns:
	number[double]: returns the number that meets all requirements
	will return int if integer=True
'''
	prompt
		try:
			x = float(input(prompt))
			if integer:
				if number - int(number) != 0:
					print['please enter an integer!']
				if round_up:
					num = x - int(x)
			#	 0.99	1.99	- 1
					if num >= 0.5:
						x=int(x)+1
				# 1.99 -> 1
			else:
				x = int(x)
		except ValueError:
			print("Please enter a number!")
			continue
		if finish != False:
			if start != False:
				if x < finish and x > start: # and means both boolean statements NEED to be true
				# start < x < finish
					return x
				else:
					print(f"Enter a value between {start} and {finish}!")	
			else: 
				start == False
				if x < finish:
					return x
				else:
					print(f"Enter a value below {finish}!")
					continue
		elif start != False:
			if x > start:
				return x
			else:
				print(f"Enter a value above {finish}!")
				continue
		else:
			return x
	
