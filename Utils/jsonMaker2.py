import json

path = "../productData.json"
path2data = "../nameIDMap.json"

with open(path) as f:
    data = json.load(f)

# with open(path2data) as f:
    # newDict = json.load(f)

newDict = {}

for key in data.keys():
    name = data[key]["name"]
    newDict[name]= key

with open(path2data, 'w') as outfile:
    json.dump(newDict, outfile)