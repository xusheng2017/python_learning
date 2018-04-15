#!/usr/bin/env python
#通用版本
import re
from distutils.log import warn as printf
import os

with os.popen('who' , 'r') as f:
	for eachLine in f:
		printf(re.split(r'\s\s+|\t' , eachLine.strip() ))