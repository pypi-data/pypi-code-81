class PersonForBMI:
	'''
	This module calculates Body Mass Index (BMI) based on a given set of parameters
	such as your weight, height, gender, age, life-style, etc.
	'''

	def __init__(self, age, weight, height, gender):

		self.age    = age
		self.weight = weight
		self.gender = gender
		self.height = height
		self.bmi = 0


	def calculate_bmi(self):
		'''
		Calculating BMI value in case you are either male or woman.
		'''

		if self.gender.upper() == 'male'.upper():
			self.bmi = self.weight / (self.height/100 * self.height/100) * 0.98
		elif gender == 'female':
			self.bmi = self.weight / (self.heigh/100 * self.height/100) * 0.94

		return self.bmi

	def conclusions(self):
		'''
		Output a conclusion based on your BMI value.
		'''
		if self.bmi < 18.5:
			print('Your weight is too low')
		elif self.bmi < 24.9:
			print('Your weight is normal.')
		elif self.bmi < 29.9:
			print('You have an overweight.')
		elif self.bmi < 34.9:
			print('1st level overweight.')
		elif self.bmi < 39.9:
			print('2nd level overweight.')
		else:
			print('3rd level overweight.')