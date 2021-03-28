def getCurrentSales(itemID):
    #TODO
    pass


def getPrediction(itemID):
    #TODO
    pass

def placeOrder(itemID):
    #TODO
    pass

def checkAvailablity(itemID):
    if(getCurrentSales(itemID) >= getPrediction(itemID)):
        placeOrder(itemID)