#!/usr/bin/python3

import re
import os

with os.popen('who' , 'r') as f:
	for eachLine in f:
		print(re.split(r'\s\s+|\t' , eachLine.strip()))