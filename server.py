from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/capturer', methods = ['POST'])
def capture():
    remote_ip = request.remote_addr
    data = request.form
    try:
        if data['confirm'] == 'success':
            #Do something with the data here
            return "Data received!"
        else:
            return "Something went wrong!"
    except:
        return "Something went wrong!"