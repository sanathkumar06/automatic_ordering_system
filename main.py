import pyrebase
import sqlite3
from flask import Flask, render_template, request, redirect, session
import os
import Query
import Payloads
import _thread
import orderManagement

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyCrigjfRyiP75zMOko_WV2ZaPWfREaDtCw",
    "authDomain": "automatic-ordering-system.firebaseapp.com",
    "databaseURL": "https://automatic-ordering-system-default-rtdb.firebaseio.com",
    "projectId": "automatic-ordering-system",
    "storageBucket": "automatic-ordering-system.appspot.com",
    "messagingSenderId": "825591819908",
    "appId": "1:825591819908:web:b6859e5983040afa101cd1",
    "measurementId": "G-QSVE0X5VC2"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

isLoggedIn = False


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global isLoggedIn
    if (request.method == 'POST'):
        email = request.form['name']
        password = request.form['password']
        try:
            auth.sign_in_with_email_and_password(email, password)
            isLoggedIn = True
            return redirect('/home')
        except:
            unsuccessful = 'Please check your credentials'
            return render_template('index.html', umessage=unsuccessful)

    return render_template('index.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        email = request.form['name']
        password = request.form['password']
        try:
            auth.create_user_with_email_and_password(email, password)
            return redirect("/index")
        except:
            unsuccessful = 'Email already exists'
            return render_template('create_account.html', umessage=unsuccessful)
    return render_template('create_account.html')


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
        email = request.form['name']
        try:
            auth.send_password_reset_email(email)
            return redirect("/index")
        except:
            unsuccessful = 'Email invalid'
            return render_template('forgot_password.html', umessage=unsuccessful)
    return render_template('forgot_password.html')


@app.route('/logout')
def logout():
    global isLoggedIn
    isLoggedIn = False
    return redirect('/')


headings = ["Item Name", "Quantity"]
headings2 = ["Item ID", "Total"]
autoheadings = ["Item Id" , "Item Name" , "Item Quantity", "Status"]


@app.route('/home', methods=['GET', 'POST'])
def home():
    if (not isLoggedIn):
        return redirect('/')

    if request.method == "GET":
        payload = Payloads.homePagePayload();
        return render_template('home.html', data=payload, headings=headings, headings2=headings2 ,headings4= autoheadings)
    else:
        item = request.form['Search']
        response = Query.lookForItem(item)
        if response == "null":
            redirectLink = "/search/" + item.replace(" ", "_")
            return redirect(redirectLink)
        else:
            redirectLink = "/item/" + response
            return redirect(redirectLink)


@app.route('/search/<string:item>', methods=['GET', 'POST'])
def searched_item(item):
    if (not isLoggedIn):
        return redirect('/')

    similar = Payloads.searchResultPayload(item)
    return render_template("searchResult.html", data=similar)


@app.route('/item/<string:id>', methods=['POST', 'GET'])
def item(id):
    if (not isLoggedIn):
        return redirect('/')

    if (request.method == 'GET'):
        payload = Payloads.itemDataPayload(id)
        # print(payload)
        return render_template("popup_alert.html", data=payload)


@app.route('/sales', methods=['POST', 'GET'])
def sales():
    if (request.method == "GET"):
        itemID = request.form["itemId"]
        quantity = request.form["quantity"]
        _thread.start_new_thread(orderManagement.processSale, (itemID, quantity))
    else:
        return render_template("sales_portal.html")


@app.route('/orderConfirm')
def liveSale():
    return render_template('orderConfirm.html')


@app.route('/liveOrders')
def liveOrders():
    return render_template('liveOrders.html')


@app.route('/queue', methods=['POST', 'GET'])
def orderQueue():
    if (request.method == "POST"):
        ID = request.form['itemId']
        print("ID==============",ID)
        quantity = request.form["itemQuantity"]
        orderManagement.placeOrderManually(ID, quantity)
        return redirect('/queue')
    else:
        return render_template('orderConfirm.html', data = Payloads.queuePayload())


@app.route('/cancel/<string:id>')
def cancel(ID):
    # TODO niki
    orderManagement.removeFromOrderQueue(ID)


if __name__ == '__main__':
    app.secret_key = "RosesAreRedSkyIsBlueFBIWantsToStealMyDickCanIHideItInsideYou"
    app.run(debug=True)
