import re
import os

f = open('whodata.txt' , 'r')

for eachLine in f:
	print( re.split(r'\s\s+|\t' , eachLine.strip()))

f.close()