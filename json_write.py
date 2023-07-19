import json


c = [None]
s = [{'a':123},{'b':c}]

with open("1.json","w") as f:
    json.dump(s,f)
    print("加载入文件完成...")

print(s)
