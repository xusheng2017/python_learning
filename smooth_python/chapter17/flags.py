#!/usr/bin/python3
#!_*_coding:utf-8_*_

#依序下载的脚本
import os
import time
import sys

import requests

POP10_CC = ('CN IN US ID BR PK NG BD RU JP').split()

BASE_URL = 'https://www.supfree.net/search.asp?id=6123'

DEST_DIR = '/home/python01/python/smooth_python/chapter17/downloads'

def save_flags(img , filename):
	path = os.path.join(DEST_DIR , filename)
	with open(path , 'wb') as fp:
		fp.write(img)

def get_flags(cc):
		url = '{}/{cc}/{cc}.gif'.format(BASE_URL , cc = cc.lower())
		resp = requests.get(url)
		return resp.content

def show(text):
	print(text, end = '')
	sys.stdout.flush()

def download_many(cc_list):
	for cc in sorted(cc_list):
		image = get_flags(cc)
		show(cc)
		save_flags(image , cc.lower() + '.gif')
	return len(cc_list)

def main(download_many):
	t0 = time.time()
	count = download_many(POP10_CC)
	elapsed = time.time() - t0
	msg = '\n{} flags downloaded in {:.2f}s'
	print(msg.format(count , elapsed))


if __name__ == '__main__':
	main(download_many)