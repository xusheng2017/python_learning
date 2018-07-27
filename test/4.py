#!/usr/bin/env python3
# -*-coding:utf-8-*-


class Student(object):
	"""docstring for Student"""
	def __init__(self, name , score):
		self.__name = name
		self.__score = score

	def get_name(self):
		return self.__name
	def get_score(self):
		return self.__score

	def set_info(self,score):
		if 0 <= score <= 100:
			self.__socre = score
		else:
			raise ValueError('bad score')


	def get_info(self):
		print('name:%s , score:%s' % (self.__name , self.__score))

	def get_grade(self):
		if self.__score > 80:
			return 'A'
		elif self.__score > 60:
			return 'B'
		else:
			return 'C'

lemon = Student('lemon' , 88)
bob = Student('bob' , 77)


print(lemon.get_info())
print(bob.get_grade())

lemon.set_info(99)
bob.set_info(50)

print(lemon.get_info())
print(bob.get_grade())