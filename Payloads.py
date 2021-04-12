import Query
from datetime import datetime
import json
import orderManagement

now = datetime.now()
pathToQueue = "Resources/orderQueue.json"
timeFormat = "%H:%M:%S"
waitTime = 60


def homePagePayload():
    payload = {}
    payload["highOnDemand"] = Query.highOnDemand(True, 10)
    payload["lowOnDemand"] = Query.highOnDemand(False, 10)
    payload["salesData"] = Query.getSalesCount()
    payload["highestEarning"] = Query.highestEarning(True, 10)
    payload["lowestEarning"] = Query.highestEarning(False, 10)
    payload["allTimeSales"] = Query.getItemSoldAllTime()
    payload["soldPerWeek"] = Query.getItemSoldPerWeek()
    payload["soldPerMonth"] = Query.getItemSoldPerMonth()
    # TODO: Nikith
    # payload["totalOrders"] = Query.getTotalOrders()

    payload["predictedSales"] = Query.getPredictedSales()
    payload['placedOrders'] = Query.getPlacedOrder()
    return payload


print(homePagePayload())

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
    payload["sales"] = Query.eachItemSoldCount(90, itemId)
    payload["prediction"] = Query.getItemPredictionFromDB(itemId)
    return payload


def liveUpdatePayload():
    return open('file.log', 'r').readlines()


def liveSalesPayload():
    # TODO: Nikith
    # recent sales
    pass


def searchResultPayload(item):
    return Query.getSimilar(item.replace("_", " "))


def queuePayload():
    with open(pathToQueue) as f:
        data = json.load(f)
    items = data.keys()
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
        if mins > waitTime:
            orderManagement.placeOrder(item, tempDict)
        else:
            tempDict['min'] = waitTime - mins
            payload[item] = tempDict

    return payload

# print(queuePayload())
