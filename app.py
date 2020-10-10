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
		with open('questions', 'rb') as f:
			questions = pickle.load(f)
			return jsonify(questions)
		return jsonify("Error")
	else:
		return render_template("practice.html")

@app.route("/processing", methods=["GET", "POST"])
def processing():
	if request.method == "POST":
		forms = []
		with open('forms', 'rb') as f:
			forms = pickle.load(f)

		offices = []
		with open('offices', 'rb') as f:
			offices = pickle.load(f)

		with open('estimations', 'rb') as f:
			estimations = pickle.load(f)
			return jsonify([forms, offices, estimations])
		return jsonify("Error")
	else:
		return render_template("processing.html")

if __name__ == "__main__":
   app.run("0.0.0.0")