import xlrd
import json
import random
import string

path = "/home/nikith/proj/automatic_ordering_system/Utils/online_retail.xlsx"

def formatCase(name):
    return name[0] + name[1:].lower()

def writeToJSON(sheet, jsonData):
    rowCount = sheet.nrows

    for i in range(1, rowCount):
        data = sheet.row_values(i)
        try:
            StockID = int(data[1])
        except:
            StockID = data[1]
            if(StockID[len(StockID) - 1].islower()):
                StockID += "1"
                print(StockID)
        try:
            nameF = formatCase(data[2])
        except:
            nameF = "Ceramic vase " + ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5))
        priceF = data[5]

        if(StockID not in jsonData.keys()):
            jsonData[StockID] = {"name":nameF, "price":priceF}


xl = xlrd.open_workbook(path)
sheet_names = xl.sheet_names()
jsonData = {}
for i in range(len(sheet_names)):
    sheet = xl.sheet_by_index(i)
    writeToJSON(sheet, jsonData)


with open('productData.json', 'w') as outfile:
    json.dump(jsonData, outfile)