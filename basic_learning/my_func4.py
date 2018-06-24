import time , functools

def metric(func):
	@functools.wraps(func)
	def wrapper(*args , **kw):
		start = time.time()
		a = func(*args , **kw)
		end = time.time()
		used_time = end - start
		print('this %s used time is %s' % (func.__name__ , used_time ))
		return a
	return wrapper

@metric
def fast(x,y):
	return x+y

@metric
def slow(x,y,z):
		return x*y*z

f = fast(11,22)
s = slow(11,22,33)

print(f,s)
