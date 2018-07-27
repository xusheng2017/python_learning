
class Student(object):
	def __init__(self , name='None' , age=0 , score=0):
		self.__name = name
		self.__age = age
		self.__score = score

	def get_name(self):
		return self.__name

	def get_age(self):
		return self.__age

	def get_score(self):
		return self.__score

	def set_name(self , name):
		self.__name = name

	def set_age(self , age ):
		self.__age = age

	def set_score(self , score):
		if 0 <= score <= 100:
			self.__score = score
		else:
			raise ValueError('bad score')

	def get_info(self):
		return self.__name , self.__age , self.__score

if __name__ == '__main__':
	main()