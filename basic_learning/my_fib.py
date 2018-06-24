def my_fib(max):
	n , a , b = 0 , 0 , 1
	while n < max:
		yield b
		a , b = b , a+b 
		n = n + 1
	return 'done'


f = my_fib(6)
for x in f:
	print(x)

g = my_fib(10)

while 1:
	try:
		x = next(g)
		print('g:' , x)
	except StopIteration as e:
		print('Genetatot return value:' , e.value)
		break