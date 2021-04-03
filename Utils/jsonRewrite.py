import json
prefix0 = "ITEM_0"
prefix = "ITEM_"

productDataPath = "../productData.json"
with open(productDataPath) as f:
    productDataJson = json.load(f)

productKeys = list(productDataJson.keys())
finalDict = {}

for i in range(1, 51):
    if(i < 10):
        itemID = prefix0 + str(i)
    else:
        itemID = prefix + str(i)

    curData = productDataJson[productKeys[i - 1]]
    name = curData["name"]
    price = curData["price"]
    distributorName = "Demo Private Limited"
    distributorMail = "demoprojectltd@gmail.com"

    finalDict[itemID]= {"name": name, "price": price, "distributorName": distributorName, "distributorMail": distributorMail}

with open('productDataUpdated.json', 'w') as outfile:
    json.dump(finalDict, outfile)