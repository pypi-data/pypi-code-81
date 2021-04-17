keys = ["keyforpro1804202110052021"]

def starttrial(seconds):
	if seconds > 100:
		print("Buy key for 10$")
		raise TypeError

	for seconds in range(0,int(seconds)):
		print(seconds)

def startpro(secondspro, key):
	if key not in keys:
		print("Invalid key!")
		raise TypeError

	for secondspro in range(0,int(secondspro)):
		print(secondspro)