import Query

def homePagePayload():
    payload = {}
    payload["highOnDemand"] = Query.highOnDemand(True)
    payload["lowOnDemand"] = Query.highOnDemand(False)
    # TODO: Vamshi :
    payload["salesData"] = Query.getSalesCount()
    payload["highestEarning"] = Query.highestEarning(True)
    payload["lowestEarning"] = Query.highestEarning(False)

    # TODO: Prasad
    # payload["totalSales"] = Query.getTotalSales()
    # TODO: Prasad
    # payload["totalOrders"] = Query.getTotalOrders()
    # TODO: Prasad
    # payload["predictedSales"] = Query.getPredictedSales()
    return payload

def salesPortalPayload():
    payload = {}
    payload["latestSales"] = Query.getLatestSales()
    payload["topSelling"] = Query.highOnDemand(True, 10)
    return payload

def itemDataPayload(itemID):
    payload = {}
    itemInfo = Query.getItemInfo(itemID)
    payload["ID"] = itemID
    payload["name"] = itemInfo["name"]
    payload["price"] = itemInfo["price"]
    payload["dates"] = Query.get_all_dates()
    payload["sales"] = Query.each_item_sold_count()
    payload["prediction"] = Query.getItemPrediction(itemID)
    return payload

def liveUpdatePayload():
    return open('file.log', 'r').readlines()

def liveSalesPayload():
    #TODO: Prasad
    # recent sales
    pass

def searchResultPayload(item):
    return Query.getSimilar(item.replace("_", " "))
