import Query
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import json

now = datetime.now()
pathToQueue = "orderQueue.json"


def sendMail(info, quantity):
    myMail = "auto.order.system@gmail.com"
    myPass = "order@123"

    msg = MIMEMultipart('alternative')
    msg['From'] = myMail
    msg['To'] = info['distributorMail']
    # todo Vamshi
    # add proper order subject and message
    # https://www.freecodecamp.org/news/send-emails-using-code-4fcea9df63f/
    msg['Subject'] = "ESCN"
    message = "Order:" + quantity
    msg.attach(MIMEText(message, 'plain'))

    # s = smtplib.SMTP("imap.gmail.com", 993)
    s = smtplib.SMTP_SSL('smtp.gmail.com')
    s.login(myMail, myPass)
    s.send_message(msg)
    s.quit()


def repredict(itemID):
    # TODO Sanath
    orderQuantity = 000
    return orderQuantity


def addToOrderQueue(itemID, quantity):
    current_time = now.strftime("%H:%M")
    info = Query.getItemInfo(itemID)
    with open(pathToQueue) as f:
        data = json.load(f)
    data[itemID] = {"time": current_time, "name": info['name'], "quantity": quantity, "price": info['price']}

    with open(pathToQueue, 'w') as outfile:
        json.dump(data, outfile)


addToOrderQueue('ITEM_05', 500)


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
