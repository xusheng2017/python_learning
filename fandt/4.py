import subprocess 

print('$ nslookup www.python.org')
r = subprocess.call(['nslookup' , 'www.python.org'])
r = subprocess.call(['nslookup' , 'www.baidu.com'])
print('exit code:' , r)