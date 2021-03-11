import json

path = "/home/nikith/proj/automatic_ordering_system/productData.json"

with open(path) as f:
    data = json.load(f)

newDict = {}

for key in data.keys():
    name = data[key]["name"]
    newDict[name]= key

with open('nameIDMap.json', 'w') as outfile:
    json.dump(newDict, outfile)