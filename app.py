import requests
from flask import Flask, request, json, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/learn")
def learn():
    return render_template("learn.html")

@app.route("/citizenship-process")
def citizenship_process():
    return render_template("citizenship_process.html")

@app.route("/visas")
def visas():
    return render_template("visas.html")

@app.route("/green-cards")
def green_cards():
    return render_template("green_cards.html")

@app.route("/practice")
def practice():
    return render_template("practice.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

if __name__ == "__main__":
   app.run("0.0.0.0")