from multiprocessing import Process , Queue
import os , time , random

def m_write(q):
	print("this is a write process (%s)" , os.getpid())
	for value in ['hello,' , 'lemon']:
		print('put %s in queue' % value)
		q.put(value)
#		time.sleep(random.random())
		time.sleep(1)
def m_read(q):
	print("this is a read process %s" , os.getpid())
	while True:
		value = q.get(True)
		print("get %s from queue" % value )

if __name__ == '__main__':
	q = Queue()
	pw = Process(target = m_write , args = (q,))
	pr = Process(target = m_read , args = (q,))
	pw.start()
	time.sleep(2)
	pr.start()
	time.sleep(10)
	pw.join()
	pr.terminate()