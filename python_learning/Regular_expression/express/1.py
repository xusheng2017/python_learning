import re , os

ex = re.findall(r'(?m)^\s+(?!noreply|postmaster)(\w+)' ,
'''
    	sales@phptr.com
		postmaster@phptr.com
		eng@phptr.com
		noreply@phptr.com
		admin@phptr.com
''')

print(ex)

ex2 =[ '%s@aw.com' % e.group(1) for e in re.finditer(r'(?m)^\s+(?!noreply|postmaster)(\w+)' ,
'''
    	sales@phptr.com
		postmaster@phptr.com
		eng@phptr.com
		noreply@phptr.com
		admin@phptr.com
''') ]

print(ex2)

