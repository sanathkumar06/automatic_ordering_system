from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/SignUp")
def SignUp():
    return render_template("signup.html")

if __name__ == "__main__":
    app.run(debug=True)