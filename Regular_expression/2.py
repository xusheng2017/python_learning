import os , re


print( bool(re.search(r'(?:(x)|(y))' , 'xy')))
print( bool(re.search(r'(?:(x)|(y))' , 'XY')))

print( bool(re.search(r'(?:(x)|(y))' , 'xx')))


