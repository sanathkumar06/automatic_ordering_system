import json

path = "/home/nikith/proj/automatic_ordering_system/productData.json"
path2data = "/home/nikith/proj/automatic_ordering_system/nameIDMap.json"

with open(path) as f:
    data = json.load(f)

# with open(path2data) as f:
    # newDict = json.load(f)

newDict = {}

for key in data.keys():
    name = data[key]["name"]
    newDict[name]= key

with open('nameIDMap.json', 'w') as outfile:
    json.dump(newDict, outfile)