from datetime import datetime

import os

pwd = os.path.abspath('.')
print('             Size    Last Modified   Name')
print('-' * 50)
for f in os.listdir(pwd):
	fsize = os.path.getsize(f)
