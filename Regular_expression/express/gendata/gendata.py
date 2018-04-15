#!/usr/bin/ env python

from random import randrange , choice
from string import ascii_lowercase as lc 
from sys import maxsize
from time import ctime

tlds = ('com' , 'edu' , 'net' , 'org' , 'gov')


for i in range(randrange(4,11)): 	#将print打印4到7次
	dt_int = randrange(2**32)    	#产生最大随机数 1970-
	dt_str = ctime(dt_int)			#将随机数转化为时间
	llen = randrange(4,8)			#将长度控制到4到7个字符
	login = ''.join(choice(lc) for j in range(llen))	#循环4到7次并将每次循环产生的随机字母加入到字符串中去
	dlen = randrange(llen,13)		#将长度控制在llen和12个字符之间
	dom = ''.join(choice(lc) for j in range(dlen)) 	#循环x到12次并将每次循环产生的随机字母加入到字符串中去
	#	时间		用户名		@		字符串dom  	.		域名 		时间长度		用户名长度 	字符串长度 	
	print('%s::%s@%s.%s::%d-%d-%d' % (dt_str , login , dom , choice(tlds) , dt_int , llen , dlen)) #依次打印对应的字符串