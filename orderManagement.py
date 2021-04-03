import sqlite3
import json
import _thread
import Query

conn = sqlite3.connect("data.db")
cur = conn.cursor()


def getCurrentSales(itemID):
    cur_sales = []
    q = "select sold from table6 where stockID = '"+ itemID +"';"
    item_sales = cur.execute(q).fetchall()
    for i in item_sales:
        cur_sales.append(i[0])
    print(cur_sales)


def placeOrder(itemID):
    distrubutor = Query.getDistributorInfo(itemID)
    # TODO Nikith


def checkAvailability(itemID):
    predictionData = json.load('prediction.json')
    if(getCurrentSales(itemID) >= predictionData[itemID]):
        placeOrder(itemID)


def processSale(itemId, quantity):
    Query.updateSalesDb(itemId, quantity)
    checkAvailability(itemId)