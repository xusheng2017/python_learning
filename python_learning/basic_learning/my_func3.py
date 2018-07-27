'''def my_addend(l = None):
	if l is None:
		l = []
'''
def my_addend(l = []):
	l.append('END')
	return l

print(my_addend([1,2,3]))
for i in range(5):
	print('count[%s] : %s' % (i , my_addend()))