def consumer():
	r = ''
	while True:
		print("r = %s" % r)
		n = yield r
		print("r = %s" % r)
		print('n=%s' % n)
		if not n:
			return
		print('[consumer] consumer %s...' % n)
		r = '200 OK'

def produce(c):
	c.send(None)
	n = 0
	while n<5:
		n = n +1
		print('[produce] produce %s...' % n)
		r = c.send(n)
		print("r = %s" % r)
		print('[produce] consumer return:%s' % r)
	c.close()

c = consumer()


produce(c)