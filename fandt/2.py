from multiprocessing import Process
import os

def run_proc(name):
	print('this is child(%s) fork %s' % (name,os.getpid()))


if __name__ == '__main__':
	print("this is father process %s" , os.getpid())
	p1 = Process(target = run_proc , args = ('test1',) )
	p2 = Process(target = run_proc , args = ('test2',) )
	print("child is run...")
	p1.start()
	p2.start()
	p1.join()
	p2.join()
	print("child end ...")
