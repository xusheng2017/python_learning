from enum import Enum , unique

class Gender(Enum):
	Male = 0
	Female = 1
#	Gender = Enum('Gender' , ('Male' , 'Famale')) 

class Student(object):
	def __init__(self , name , gender):
		self.name = name
		self.gender = gender


s = Student('lemon' , Gender.Male.value)
print(s.name , s.gender)