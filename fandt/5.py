import subprocess 

#print('$ nslookup www.python.org')
print("$ nslookup")
p = subprocess.Popen(['nslookup'] , stdin = subprocess.PIPE , stdout = subprocess.PIPE , stderr = subprocess.PIPE)
output , err = p.communicate(b'set q=mx\nbaidu.com\nexit\n')
print(output.decode('utf-8'))

#r = subprocess.call(['nslookup' , 'www.python.org'])
#r = subprocess.call(['nslookup' , 'www.baidu.com'])
#print('exit code:' , r)
print('exit code:' , p.returncode)