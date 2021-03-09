import pyrebase
import sqlite3
from flask import Flask, render_template, request, redirect, session
import os
import Query

app = Flask(__name__)

config = {
    "apiKey" : "AIzaSyCrigjfRyiP75zMOko_WV2ZaPWfREaDtCw",
    "authDomain" : "automatic-ordering-system.firebaseapp.com",
    "databaseURL" : "https://automatic-ordering-system-default-rtdb.firebaseio.com",
    "projectId" : "automatic-ordering-system",
    "storageBucket" : "automatic-ordering-system.appspot.com",
    "messagingSenderId" : "825591819908",
    "appId" : "1:825591819908:web:b6859e5983040afa101cd1",
    "measurementId" : "G-QSVE0X5VC2"
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
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return redirect("/index")
            
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return redirect("/index")

    return render_template('forgot_password.html')

@app.route('/logout')
def logout():
    global isLoggedIn
    isLoggedIn = False
    return redirect('/')


headings = ("StockID")

@app.route('/home', methods=['GET', 'POST'])
def home():
    global isLoggedIn
    dates_desc = []
    if(isLoggedIn):
        dates = Query.getLast7dates()

        high_sales = Query.highOnDemand(dates, True, 7)
        low_sales = Query.highOnDemand(dates, False, 7)

        return render_template('home.html', high_on_demand = high_sales, low_on_demand = low_sales, headings = headings)
    else:
        return redirect('/')

@app.route('/searched_item', methods =  ['GET', 'POST'])
def searched_item():
    #global isLoggedIn
    #if(isLoggedIn):
    if(request.method == 'GET'):
        item = request.args.get("Search")
        # print(item)
        if(item == ""):
            return redirect("/home")
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            tot_sales = cur.execute("select * from table3 where stockID = :id;", {"id" : item}).fetchall()
        return render_template("searched_item.html", dat = item, details = tot_sales)
    else:
        return redirect('/home')

@app.route('/item/<string:id>', methods = ['POST', 'GET'])
def item(id):
    if(request.method == 'GET'):
        f = request.args.get("From")
        t = request.args.get("To")        
        return render_template("popup_alert.html", path = id, f = f, t = t)

@app.route('/sales', methods = ['POST', 'GET'])
def sales():
    if(request.method == "GET"):
        item = request.args.get("Search")
        quan = request.args.get("quantity")
        with sqlite3.connect("data.db") as con:
            cur = con.cursor()
            cur.execute("insert into table5(:item, :quan);",{"item":item, "quan": quan})
            con.commit()
        return render_template("sales_portal.html")


@app.route('/liveSales')
def liveSale():
    render_template('liveSales.html')
        
if __name__ == '__main__':
    app.secret_key = "yourppisveryverysmall"
    app.run(debug=True)
