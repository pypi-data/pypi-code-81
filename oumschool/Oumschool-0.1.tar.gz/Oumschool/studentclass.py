# studentclass.py

class Student:
	def __init__(self, name): # self คือตัวแทน
		self.name = name
		# student1.name
		# self = student1
		self.exp = 0
		self.lesson = 0
		# Call Function
		#self.AddExp(10)

	def Hello(self):
		print('สวัสดีจ้าาา ผมชื่อ {}'.format(self.name))

	def Coding(self):
		print('{} : กำลังเขียนโปรแกรม'.format(self.name))
		self.exp += 5
		self.lesson += 1

	def ShowExp(self):
		print('- {} มีประสบการณ์ {} exp'.format(self.name, self.exp))
		print('- เรียนไป {} ครั้งแล้ว'.format(self.lesson))

	def AddExp(self, score):
		self.exp += score # self.exp = self.exp + score
		self.lesson += 1


class SpecialStudent(Student):

	def __init__(self, name, father):
		super().__init__(name)
		self.father = father
		mafia = ['Bill Gates', 'Thomas Edison']
		if father in mafia:
			self.exp += 100

	def AddExp(self, score):
		self.exp += (score*3)
		self.lesson += 1

	def AskExp(self, score=10):
		print('ครู !! ขอคะแนนพิเศษให้ผมหน่อยสิ่ {} Exp'.format(score))
		self.AddExp(score)


if __name__ == '__main__':
	print('========1 Jan=========')
	student0 = SpecialStudent('Mark Zuckerberg', 'Bill Gates')
	student0.AskExp()
	student0.ShowExp()


	student1 = Student('Albert')
	print(student1.name)
	student1.Hello()

	print('----------------')

	student2 = Student('Steve')
	print(student2.name)
	student2.Hello()

	print('========2 Jan=========')

	print('-------uncle: ใครอยากเรียน Coding บ้าง--------(10  exp)---------')

	student1.AddExp(10)

	print('========3 Jan=========')
	print('ตอนนี้ exp ของแต่ละคนได้เท่าไรกันแล้ว')

	print(student1.name, student1.exp)
	print(student2.name, student2.exp)

	print('========4 Jan=========')
	for i in range(5):
			student2.Coding()

	student2.ShowExp()
	student1.ShowExp()