#!usr/bin/env python3


import ftplib
import os
import socket

HOST = 'ftp.mozilla.org'
DIRN = '/home/python01/python/python_learning/ftp'
FILE = 'bugzilla-LATEST.tar.gz'


def main():
	try:
		f = ftplib.FTP(HOST)
	except (socket.error , socket.gaierror) as e:
		print("ERROR:cannot reach %s % HOST")
		return 
	print("***connect to host %s % HOST")

	try:
		f.login()
	except ftp.error_prem:
		print("ERRIR:cannot lodin anonymous")
		f.quit()
		return 
	print("***login in as 'annonymous'")

	try:
		f.cwd(DRIN)
	except ftp.error_prem:
		print("ERROR:cannot CD to '%s' % DIRN")
		f.quit()
		return 
		raise e
	print("***change to '%s' folder" % DIRN)

	try:
		f.retrbinary('RETR %s' % FILE , open(FILE,'wb').write)
	except ftplib.error_prem:
		print("ERROR: cannot read file '%s'" % FILE)
		os.unlink(FILE)
		raise e
	else:
		print("*** Downloaded '%s' to CWD" % FILE)
		f.quit()

if __name__ == '__main__':
	main()