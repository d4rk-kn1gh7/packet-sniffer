from flask import Flask, render_template, request, redirect, json, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sniffer_data"
mongo = PyMongo(app)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/capturer', methods = ['POST'])
def capture():
    remote_ip = request.remote_addr
    data = request.form.to_dict()
    print(data)
    try:
        if request.form['confirm'] == 'success':
            mongo.db.request_data.insert_one(data)
            return "Data Received!"
        else:
            return "No Data :P"
    except:
        return "No Data :p"

@app.route('/display')
def display():
    return "i'll do this later"
