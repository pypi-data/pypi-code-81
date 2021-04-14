# -*- coding: utf-8 -*-

class Student:
    def __init__(self,name,lastname):
        self.name = name
        self.lastname = lastname
        self.exp = 0
        self.lesson = 0
        self.vehicle = 'Bus'

    @property
    def fullname(self):
        return '{} {}'.format(self.name,self.lastname)


    def Coding(self):
        '''This is class programming'''
        self.AddExp()
        print('{} Programing learning...'.format(self.fullname))

    def ShowExp(self):
        print('{} point {} exp (learn {} lesson )'.format(self.name, self.exp,self.lesson))

    def AddExp(self):
        self.exp += 10
        self.lesson += 1

    def __str__(self):
        return self.fullname
    def __repr__(self):
        return self.fullname
    def __add__(self,other):
        return self.exp + other.exp

class SpecialStudent(Student):
    def __init__(self,name,lastname,father):
        super().__init__(name,lastname)

        self.father = father
        self.vehicle = Tesla()
        print('Who i am ? my dad {}'.format(self.father))
    def AddExp(self):
        self.exp +=30
        self.lesson += 2

class Teacher:
    def __init__(self,fullname):
        self.fullname = fullname
        self.students = []

    def CheckStudent(self):
        print('--student of {}-----'.format(self.fullname))
        for i,st in enumerate(self.students):
            print('{} --> {} [ {} exp][learn {} time ] '.format(i+1,st.fullname,st.exp,st.lesson))

    def AddStudent(self,st):
        self.students.append(st)



class Tesla:
    def __init__(self):
        self.model = 'Tesla Model S'
    def SelfDriving(self,st):
        print('System autonomous working....bring Mr. {} back home'.format(st.name))
    def __str__(self):
        return self.model


if __name__ =='__main__':

    #Day0
    print('---- Day0 ----')
    allstudent = []
    teacher1 = Teacher(fullname='Ada lovelace')
    teacher2 = Teacher(fullname='Bill Gates')
    print(teacher1.students)



    #Day 1
    print('---- Day1 ----')
    st1 = Student('Albert','Einstein')
    allstudent.append(st1)
    teacher2.AddStudent(st1)
    print(st1.fullname)


    #Day2
    print('---- Day2 ----')
    st2 = Student('Steve','jobs')
    allstudent.append(st2)
    teacher2.AddStudent(st2)
    print(st2.fullname)

    #Day3
    print('---- Day3 ----')
    for i in range(3):
        st1.Coding()
    st2.Coding()
    st1.ShowExp()
    st2.ShowExp()

    #Day4
    print('---- Day4 ----')
    stp1 = SpecialStudent('Thomas','Edison','Hitler')
    allstudent.append(stp1)
    teacher1.AddStudent(stp1)
    print(stp1.fullname)
    print('May i give special 20 point?')
    stp1.exp = 20
    stp1.Coding()
    stp1.ShowExp()

    #Day5
    print('---- Day5 ----')
    print('How student back home with...')
    print(allstudent)

    for st in allstudent:
        print(' {} : Back home with {} '.format(st.name,st.vehicle))
        if isinstance(st,SpecialStudent):
            st.vehicle.SelfDriving(st)

    #Day6
    print('---- Day6 ----')

    teacher1.CheckStudent()
    teacher2.CheckStudent()

    print('Total point 2 student ',st1+st2)



