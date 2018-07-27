import os
import json

d = dict(name = 'Lemon',age = 18 , score = 88)

print(json.dumps(d))


json_str = json.dumps(d)
print(json_str)

print(json.loads(json_str))
