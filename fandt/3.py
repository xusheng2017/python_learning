#from multiprocessing import Process
from multiprocessing import Pool
import os , time , random

def long_time_task(name):
	print("child(%s) has running(%s)..." % (name , os.getpid()))
	start = time.time()
	time.sleep(1)
	end = time.time()
	print("this child(%s) has run %s second" % (name , (end-start) ))


if __name__ == '__main__':
	print("parent has running...(%s)" , os.getpid())
	p = Pool(5)
	for i in range(5):
		p.apply_async(long_time_task , args = (i,))
	print("wait child fork end...")
	p.close()
	p.join()
	print("all fork end...")