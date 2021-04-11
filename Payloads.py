import Query
from datetime import datetime
import json
import orderManagement

now = datetime.now()
pathToQueue = "orderQueue.json"
timeFormat = "%H:%M:%S"

def homePagePayload():
    payload = {}
    payload["highOnDemand"] = Query.highOnDemand(True, 10)
    payload["lowOnDemand"] = Query.highOnDemand(False, 10)
    # TODO: Vamshi :
    # payload["salesData"] = Query.getSalesCount()
    payload["highestEarning"] = Query.highestEarning(True, 10)
    payload["lowestEarning"] = Query.highestEarning(False, 10)
    # TODO: Prasad
    # p ayload["totalSales"] = Query.getTotalSales()
    # TODO: Prasad
    # payload["totalOrders"] = Query.getTotalOrders()
    # TODO: Sanath
    # payload["predictedSales"] = Query.getPredictedSales()
    return payload

def salesPortalPayload():
    payload = {}
    # payload["latestSales"] = Query.getLatestSales()
    payload["topSelling"] = Query.highOnDemand(True, 10)
    return payload

def itemDataPayload(itemId):
    payload = {}
    itemInfo = Query.getItemInfo(itemId)
    payload["ID"] = itemId
    payload["name"] = itemInfo["name"]
    payload["price"] = itemInfo["price"]
    payload["dates"] = Query.getAllTheDates()
    # payload["sales"] = Query.each_item_sold_count()
    # TODO: Sanath
    #  Predicted sales for the item
    # payload["prediction"] = Query.getItemPrediction()
    return payload

def liveUpdatePayload():
    return open('file.log', 'r').readlines()

def liveSalesPayload():
    #TODO: Prasad
    # recent sales
    pass

def searchResultPayload(item):
    return Query.getSimilar(item.replace("_", " "))

def queuePayload():
    with open(pathToQueue) as f:
        data = json.load(f)
    items = data.keys()
    print(items)
    payload = {}
    current_time = now.strftime("%H:%M:%S")
    for item in items:
        info = Query.getItemInfo(item)
        time = datetime.strptime(current_time, timeFormat) - datetime.strptime(data[item]['time'], timeFormat)
        tempDict = {}
        mins = time.seconds // 60
        tempDict['name'] = info['name']
        tempDict['quantity'] = data[item]['quantity']
        tempDict['cost'] = data[item]['quantity'] * info['price']
        if mins > 5:
            orderManagement.placeOrder(item, tempDict)
        else:
            tempDict['min'] = mins
            payload[item] = tempDict

    return payload


queuePayload()

