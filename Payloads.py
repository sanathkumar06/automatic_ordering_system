import Query

def homePagePayload():
    payload = {}
    payload["highOnDemand"] = Query.highOnDemand(True, 7)
    payload["lowOnDemand"] = Query.highOnDemand(False, 7)
    payload["salesData"] = Query.getSalesCount()
    payload["highestEarning"] = Query.highestEarning(True)
    payload["lowestEarning"] = Query.highestEarning(False)

    # TODO: Below 3
    payload["totalSales"] = Query.getTotalSales()
    payload["totalOrders"] = Query.getTotalOrders()
    payload["predictedSales"] = Query.getPredictedSales()
    return payload

def salesPortalPayload():
    payload = {}
    #TODO: getLatestSales
    payload["latestSales"] = Query.getLatestSales()
    payload["topSelling"] = Query.highOnDemand(True, 10)
    return payload

def itemDataPayload(itemId):
    itemInfo = Query.getItemInfo(itemId)
    payload = {}
    payload["ID"] = itemId
    payload["name"] = itemInfo["name"]
    payload["price"] = itemInfo["price"]
    payload["dates"] = Query.get_all_dates()
    payload["sales"] = Query.each_item_sold_count()
    #payload["prediction"] = TODO:Predicted sales for the item
    return payload

def liveUpdatePayload():
    return open('file.log', 'r').readlines()

def liveSalesPayload():
    #TODO: recent sales

def searchResultPayload():
    return Query.getSimilar(item.replace("_", " "))
