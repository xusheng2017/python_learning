
while True:
	try:
		salary = int(input("please inpurt:>>>"))
	except:
		if salary >= 10000:
			print('a')
		elif salary >= 8000:
			print('b')
		elif salary >= 6000:
			print('c')
		else:
			print('d')
