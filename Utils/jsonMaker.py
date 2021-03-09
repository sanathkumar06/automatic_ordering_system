import xlrd
import json

path = "/home/nikith/proj/automatic_ordering_system/Utils/online_retail.xlsx"

xl = xlrd.open_workbook(path)
sheet = xl.sheet_by_index(0)
rowCount = sheet.nrows

jsonData ={}

for i in range(1, rowCount):
    data = sheet.row_values(i)
    try:
        StockID = int(data[1])
    except:
        StockID = data[1]
    nameF = data[2]
    priceF = data[5]

    if(StockID not in jsonData.keys()):
        jsonData[StockID] = {"name":nameF, "price":priceF}

with open('productData.json', 'w') as outfile:
    json.dump(jsonData, outfile)

