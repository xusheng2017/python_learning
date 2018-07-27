import requests

r = requests.get('https://www.baidu.com/s?wd=python&ie=utf-8&tn=96327163_hao_pg' , params = {'q':'python' , 'cat' : '1001'})

print(r.status_code , r.url ,r.cookies['ts'])

h = r.headers
print(h)

for k, v in h.items():
	print(k ,':' , v)