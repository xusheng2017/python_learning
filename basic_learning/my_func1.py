#!/bin/usr/python3
#求一元二次函数的解

import math

def func1(a , b , c):
	if not isinstance(a,(int , float)):
		raise TypeError('bad operate type')
	if not isinstance(a,(int , float)):
		raise TypeError('bad operate type')
	if not isinstance(a,(int , float)):
		raise TypeError('bad operate type')
	delta = b*b -4*a*c
	print(delta)
	if delta < 0:
		print('this func has no result')
	elif delta == 0:
		x = (-b)/2
		return x
	else:
		x1 = (-b - math.sqrt(delta))/2
		x2 = (-b + math.sqrt(delta))/2
		return x1 , x2	

print('please input three numbers\n')
a = float(input('>>>'))
b = float(input('>>>'))
c = float(input('>>>'))

print(func1(a,b,c))