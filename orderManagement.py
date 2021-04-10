import sqlite3
# import Query
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(info, quantity):
    myMail = "auto.order.system@gmail.com"
    myPass = "order@123"

    msg = MIMEMultipart('alternative')
    msg['From'] = myMail
    msg['To'] = info['distributorMail']
    #todo Vamshi
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

info = {'distributorMail': "nikithks007@gmail.com"}
sendMail(info, '5000')

def placeOrder(itemID):
    itemInfo = Query.getItemInfo(itemID)
    # TODO Sanath
    orderQuantity = 000
    sendMail(itemInfo, orderQuantity)


def checkAvailability(itemID):
    predictionData = Query.getItemPrediction(itemID)
    if Query.getCurrentSales(itemID) >= predictionData[itemID]:
        placeOrder(itemID)


def processSale(itemId, quantity):
    Query.updateSalesDb(itemId, quantity)
    checkAvailability(itemId)
