import sqlite3
import Query
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import json

now = datetime.now()
pathToQueue = "Resources/orderQueue.json"
pathToPlacedOrder = "Resources/placedOrders.json"
pathToLogFile = "Resources/recentLogs.txt"

# Function to send mail to distributor request for prduct
def sendMail(itemID, quantity):
    info = Query.getItemInfo(itemID)
    myMail = "auto.order.system@gmail.com"
    myPass = "order@123"

    msg = MIMEMultipart('alternative')
    msg['From'] = myMail
    msg['To'] = info['distributorMail']
    msg['Subject'] = "Order Deliviery Required"

    message = "Hello Distritutor," + "\n" + "The Order of Item " + info[
        'name'] + "Has been placed by the customer for" + " " + quantity + " " + "Quantities" + "\n" + "Request you to Dispach the Order As Soon As Possible" + "\n" + "\n" + "- Auto Ordering Company"
    msg.attach(MIMEText(message, 'plain'))

    # s = smtplib.SMTP("imap.gmail.com", 993)
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(myMail, myPass)
    s.send_message(msg)
    s.quit()

# Function returns prediction for single item for next 7 days
def repredict(itemID):
    orderQuantity = Query.intermediatePrediction(itemID, 7)
    return orderQuantity

# Add a item to to be ordered queue
def addToOrderQueue(itemID, quantity):
    current_time = now.strftime("%H:%M:%S")
    info = Query.getItemInfo(itemID)
    with open(pathToQueue) as f:
        data = json.load(f)
    data[itemID] = {"time": current_time, "quantity": quantity}

    with open(pathToQueue, 'w') as outfile:
        json.dump(data, outfile)


# addToOrderQueue('ITEM_03', 1000)
# addToOrderQueue('ITEM_07', 700)
# addToOrderQueue('ITEM_27', 770)

# Add a new message to logs file, remove old logs if it is more than limit
def addToLogs(message):
    with open(pathToLogFile, 'r') as f:
        data = f.readlines()

    try:
        data.pop(10)
    except Exception:
        pass

    data.insert(0, message + "\n")
    with open(pathToLogFile, 'w') as f:
        f.write(''.join(data))


# addToLogs("ESCN")

# Remove a order from order queue
def removeFromOrderQueue(itemID):
    with open(pathToQueue) as f:
        data = json.load(f)
    data.pop(itemID)
    with open(pathToQueue, 'w') as outfile:
        json.dump(data, outfile)

# Remove a order data from placed orders
def removeFromPlacedOrders(itemID):
    with open(pathToPlacedOrder) as f:
        data = json.load(f)
    info = data.pop(itemID)
    with open(pathToPlacedOrder, 'w') as outfile:
        json.dump(data, outfile)
    return info['quantity']

# Update placed order file with new order
def updateToOrdered(itemID, info):
    with open(pathToPlacedOrder) as f:
        data = json.load(f)
    print(data)
    data[itemID] = info
    with open(pathToPlacedOrder, 'w') as outfile:
        json.dump(data, outfile)

# Calls all necessary functions for placing order and updating the information
# Is called when the system places order after wait time
def placeOrder(itemID, data):
    addToLogs('Order placed for {0} units of {1} automatically.'.format(data['quantity'], itemID))
    sendMail(itemID, str(data['quantity']))
    updateToOrdered(itemID, data)
    removeFromOrderQueue(itemID)

# Calls all necessary functions for placing order and updating the information
# Is called when order is placed manually by the user from UI
def placeOrderManually(itemID, quantity):
    sendMail(itemID, str(quantity))
    data = {}
    info = Query.getItemInfo(itemID)
    data['name'] = info['name']
    data['quantity'] = quantity
    data['cost'] = int(quantity) * info['price']
    updateToOrdered(itemID, data)
    removeFromOrderQueue(itemID)

# Check if there is enough stock to meet demand
def checkAvailability(itemID):
    predictionData = Query.getItemPrediction(itemID)
    if Query.getCurrentSales(itemID) >= predictionData:
        currentStock = Query.getCurrentStock(itemID)
        newPrediction = repredict(itemID)
        if newPrediction > currentStock:
            addToOrderQueue(itemID, newPrediction - currentStock)

# Calls functions to update information after a sale and logs the sale
def processSale(itemId, quantity):
    addToLogs(quantity + " units of " + itemId + " was sold.")
    Query.updateSalesDb(itemId, quantity)
    Query.updateCurrentStocks(itemId, quantity)
    checkAvailability(itemId)
