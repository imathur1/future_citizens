import pickle
import requests
from flask import Flask, request, json, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/naturalization")
def naturalization():
    return render_template("naturalization.html")

@app.route("/green-cards")
def green_cards():
    return render_template("green_cards.html")

@app.route("/practice", methods=["GET", "POST"])
def practice():
    if request.method == "POST":
        with open ('questions', 'rb') as fp:
            questions = pickle.load(fp)
            return jsonify(questions)
        return jsonify("Error")
    else:
        return render_template("practice.html")

@app.route("/calculator")
def calculator():
    return render_template("calculator.html")

if __name__ == "__main__":
   app.run("0.0.0.0")