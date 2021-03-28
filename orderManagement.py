import sqlite3

conn = sqlite3.connect("data.db")
cur = conn.cursor()

def getCurrentSales(itemID):
    cur_sales = []
    q = "select target from table6 where stockID = '"+ itemID +"';"
    item_sales = cur.execute(q).fetchall()
    for i in item_sales:
        cur_sales.append(i[0])
    print(cur_sales)

def getPrediction(itemID):
    #TODO
    pass

def placeOrder(itemID):
    #TODO
    pass

# def checkAvailablity(itemID):
#     if(getCurrentSales(itemID) >= getPrediction(itemID)):
#         placeOrder(itemID)
