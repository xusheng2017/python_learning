from collections import deque

l = [0,1,2,3,4,5,6,7,8,9]
l = list(range(10))
print('l = %s' % l)


q = deque(l,10)
q.append(11)
print(q)
q.appendleft(12)
print(q) 

q.pop()
print(q)
q.popleft()
print(q)