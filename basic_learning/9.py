import logging
logging.basicConfig(level = logging.INFO)#DEBUG WARMING ERROR
'''
def func():
	n = int(input('>>> '))
	assert n != 0 , 'n is zero'
	print(10 / n)
'''

s = input('>>>')
n = int(s)

logging.info('n = %d' % n )
print(10 / n)

'''
if __name__ == '__main__':
	func()
'''