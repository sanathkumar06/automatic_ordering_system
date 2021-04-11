import sqlite3
import Query
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import json

now = datetime.now()
pathToQueue = "orderQueue.json"
pathToPlacedOrder = "placedOrders.json"


def sendMail(info, quantity):
    myMail = "auto.order.system@gmail.com"
    myPass = "order@123"

    msg = MIMEMultipart('alternative')
    msg['From'] = myMail
    msg['To'] = info['distributorMail']
    # add proper order subject and message
    # https://www.freecodecamp.org/news/send-emails-using-code-4fcea9df63f/
    msg['Subject'] = "Order Deliviery Required"
    
    message = "Hello Distritutor," + "\n" + "The Order of Item " + "itemname" + "Has been placed by the customer for" + " " +quantity + " " +"Quantities" + "\n" + "Request you to Dispach the Order As Soon As Possible" + "\n" + "\n" + "- Auto Ordering Company"
    msg.attach(MIMEText(message, 'plain'))

    # s = smtplib.SMTP("imap.gmail.com", 993)
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(myMail, myPass)
    s.send_message(msg)
    s.quit()

info = {'distributorMail': "vamshi123pv@gmail.com"}
sendMail(info, '5000')


def repredict(itemID):
    # TODO Sanath
    orderQuantity = 000
    return orderQuantity


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


def removeFromOrderQueue(itemID):
    with open(pathToQueue) as f:
        data = json.load(f)

    data.pop(itemID)
    with open(pathToQueue, 'w') as outfile:
        json.dump(data, outfile)


def updateToOrdered(itemID, info):
    with open(pathToPlacedOrder) as f:
        data = json.load(f)

    data[itemID] = info
    with open(pathToPlacedOrder, 'w') as outfile:
        json.dump(data, outfile)


def placeOrder(itemID, data):
    sendMail(Query.getItemInfo(itemID), str(data['quantity']))
    updateToOrdered(itemID, data)
    removeFromOrderQueue(itemID)


def checkAvailability(itemID):
    predictionData = Query.getItemPrediction(itemID)
    if Query.getCurrentSales(itemID) >= predictionData[itemID]:
        currentStock = Query.getCurrentStock(itemID)
        newPrediction = repredict(itemID)
        if newPrediction > currentStock:
            addToOrderQueue(itemID, currentStock)


def processSale(itemId, quantity):
    Query.updateSalesDb(itemId, quantity)
    checkAvailability(itemId)
