#!/bin/usr/python3 

def my_power(x , n = 2):
	s = 1
	while n > 0:
		n = n-1
		s = s*x
	return s

print('power(5)=%s' % my_power(5))
print('power(5,3)=%s' % my_power(5,3))