import sqlite3
import Query
import smtplib
from email.message import EmailMessage


def sendMail(info, quantity):
    myMail = "fake1@gmail.com"
    email = smtplib.SMTP(info["distributorMail"], 587)
    email.starttls()
    email.login(myMail, "sender_password")
    # message = EmailMessage()
    # message['Subject'] = "Order stuff"
    msg = "Order:" + quantity
    email.sendmail(myMail, info["distributorMail"], msg)


def placeOrder(itemID):
    itemInfo = Query.getItemInfo(itemID)
    # todo Sanath
    orderQuantity = 000
    sendMail(itemInfo, orderQuantity)


def checkAvailability(itemID):
    predictionData = Query.getItemPrediction(itemID)
    if Query.getCurrentSales(itemID) >= predictionData[itemID]:
        placeOrder(itemID)


def processSale(itemId, quantity):
    Query.updateSalesDb(itemId, quantity)
    checkAvailability(itemId)
