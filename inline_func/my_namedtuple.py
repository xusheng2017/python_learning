from collections import namedtuple

point = namedtuple('point' , ['x' , 'y'])
p = point(1,2)
print(type(p))
print('px = %s py = %s ' % (p.x , p.y))