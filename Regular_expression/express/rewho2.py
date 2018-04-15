#!/usr/bin/python3
import re
import os

f = os.popen('who' , 'r')

for eachLine in f:
	print( re.split(r'\s\s+|\t' , eachLine.rstrip()))

f.close()



