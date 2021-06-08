from flask import Flask, render_template, request, redirect, json, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/sniffer_data"
mongo = PyMongo(app)

@app.route('/')
def home():
    return render_template("index.html")

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
    bar_labels=""
    bar_values=""
    pie_values=""
    pie_labels=""
    if (request.method == 'POST'):
        device_name=request.form['device-select']
        update=True
        bar_labels, bar_values= get_bar_chart_val(mongo.db.website_data, device_name)
        pie_values= get_pie_chart_val(mongo.db.website_data, device_name)
        #print(bar_labels)
        #print(bar_values)
    return render_template("dashboard.html", 
                            website_data=mongo.db.website_data,
                            update=update,
                            device_name=device_name,
                            bar_labels=bar_labels,
                            bar_values=bar_values,
                            pie_values=pie_values,)

@app.route('/datadump', methods=['POST', 'GET'])
def display_datadump():
    update=False
    device_name=""
    if (request.method == 'POST'):
        device_name=request.form['device-select']
        update=True
    return render_template("datadump.html",
                            tcpdump_data=mongo.db.tcpdump_data,
                            update=update,
                            device_name=device_name
                            )

def get_bar_chart_val(website_data, device_name):
    labels=website_data.distinct("website", {"device_name":device_name})
    if "" in labels:
        labels.remove("")
    values=[]
    for data in labels:
        values.append(website_data.find({"website":data}).count())
    return labels, values

def get_pie_chart_val(website_data, device_name):
    sites=website_data.distinct("website", {"device_name":device_name})
    count=0
    if "" in sites:
        sites.remove("")
    for item in sites:
        if ".edu" not in item:
            count+=1
    total_val=len(sites)
    values=[total_val-count, count]
    return values