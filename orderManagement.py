import sqlite3
import json

conn = sqlite3.connect("data.db")
cur = conn.cursor()

distributors = json.load("distributors.")

def getCurrentSales(itemID):
    cur_sales = []
    q = "select sold from table6 where stockID = '"+ itemID +"';"
    item_sales = cur.execute(q).fetchall()
    for i in item_sales:
        cur_sales.append(i[0])
    print(cur_sales)


def getDistributorInfo(itemID):
    # TODO


def placeOrder(itemID):
    distrubutor = getDistributorInfo(itemId)
    # TODO order

def checkAvailablity(itemID):
    predictionData = json.load('prediction.json')
    if(getCurrentSales(itemID) >= predictionData[itemID]):
        placeOrder(itemID)
