import os

pid = os.fork()
print("os.fork return %s" , pid) #child ==0 father == child pid
if pid == 0:
	print("this is child fork(%s)" ,os.getpid())
else:
	print("this is father fork(%s)" , os.getpid())

