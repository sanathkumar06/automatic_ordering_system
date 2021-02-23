import pyrebase
from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)

#firebase credentials
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
cred = []
invalid = True

@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    global invalid
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            global cred
            try:
                auth.sign_in_with_email_and_password(email, password)
                #print(email)
                #print(email[::5])
                #cred[0] = email
                #cred[1] = password
                return render_template('home.html')
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
            return render_template('index.html')
    return render_template('create_account.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('index.html')
    return render_template('forgot_password.html')


@app.route('/home', methods=['GET', 'POST'])
def home():
    if(invalid == False):
        return render_template('home.html')
    else:
        return render_template("error.html")


if __name__ == '__main__':
    app.secret_key = "yourppisveryverysmall"
    app.run(debug=True)
