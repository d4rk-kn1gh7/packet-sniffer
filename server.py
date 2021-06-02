from flask import Flask, render_template, request, redirect, json, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sniffer_data"
mongo = PyMongo(app)

app = Flask(__name__)

@app.route('/')
def home():
    return ("Visit the Dashboard for more info (/dashboard)")

@app.route('/capturer', methods = ['POST'])
def capture():
    remote_ip = request.remote_addr
    data = request.form.to_dict()
    try:
        if request.form['confirm'] == 'success':
            if "website" in data:
                mongo.db.website_data.insert_one(data)
            mongo.db.tcpdump_data.insert_one(data)
            return "Data Received!"
        else:
            return "No Data :P"
    except Exception as e:
        return e

@app.route('/dashboard', methods=['POST', 'GET'])
def display_dashboard():
    update=False
    device_name=""
    labels=""
    values=""
    max_val=""
    if (request.method == 'POST'):
        device_name=request.form['device-select']
        update=True
        labels, values= get_chart_val(mongo.db.website_data, device_name)
        max_val=max(values)
    return render_template("dashboard.html", 
                            website_data=mongo.db.website_data,
                            update=update,
                            device_name=device_name,
                            labels=labels,
                            values=values,
                            max=max_val)

@app.route('/datadump')
def display_datadump():
    return render_template("datadump.html")

def get_chart_val(website_data, device_name):
    labels=website_data.distinct("website", {"device_name":device_name})
    if "" in labels:
        labels.remove("")
    values=[]
    for data in labels:
        values.append(website_data.find({"website":data}).count())
    return labels, values
