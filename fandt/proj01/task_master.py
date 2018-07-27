import random , time , queue
from multiprocessing.managers import BaseManager
#发送任务的队列
task_queue = queue.Queue()
#接受结构的队列
result_queue = queue.Queue()

class QueueManager(BaseManager):
	pass
#把两个队列都注册到网上
QueueManager.register('get_task_queue' , callable = lambda: task_queue)
QueueManager.register('get_result_queue' , callable = lambda:result_queue)
#绑定端口 设置验证码
manager = QueueManager(address=('' , 5000) , authkey = b'abc')

manager.start()
#获得通过网络访问的queue对象
task = manager.get_task_queue()
result = manager.get_result_queue()
#放几个任务进去
for i in range(10):
		n = random.randint(0,10000)
		print('Put task %d...' % n)
		task.put(n)
#从result队列读取结果
print('Try get results...')

for i in range(10):
	r = result.get(timeout=100)
	print('Result:%s' % r)

manager.shutdown()
print('master exit.')
