import pickle

d = dict(name = 'Lemon',age = 18,score = 88)
data = pickle.dumps(d)
print(data)

re_date = pickle.loads(data)
print(re_date)