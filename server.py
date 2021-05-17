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
            return render_template("capturer.html, success=True", data=data, errorMsg=None)
        else:
            return render_template("capturer.html, success=False", data=data, errorMsg="")
    except:
        return render_template("capturer.html, success=Falsee", data=data, errorMsg="")
