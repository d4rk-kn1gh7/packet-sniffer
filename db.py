from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'test'
app.config['MONGO_URI'] = 'mongodb+srv://sreeragkvivek:sreerag3907@cluster0.anqga.mongodb.net/test?authSource=admin&replicaSet=atlas-p9u97s-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true'

mongo = PyMongo(app)

@app.route('/star', methods=['POST'])
def add_star():
  star = mongo.db.stars
  ethproto = request.json['ethproto']
  netproto = request.json['netproto']
  src_ip = request.json['src_ip']
  device_name = request.json['device_name'] 
  dest_ip = request.json['dest_ip']
  src_port = request.json['src_port']
  dest_port= request.json['dest_port']
  website=request.json['website']
  confirm = request.json['confirm']

  star_id = star.insert({'ethproto': ethproto, 'netproto': netproto,"src_ip":src_ip,"dest_ip":dest_ip,"src_port":src_port,"dest_port":dest_port,"website":website,"device_name":device_name,"confirm":confirm})
  new_star = star.find_one({'_id': star_id })
  output = {'ethproto' : new_star['ethproto'], 'netprorto' : new_star['netproto'],'src_ip':new_star['src_ip'],'dest_ip':new_star['dest_ip'],'src_port':new_star['src_port'],'website':new_star['website'],'dest_port':new_star['dest_port'],'device_name':new_star['device_name'],'confirm':new_star['confirm']}
  return jsonify({'result' : output})

@app.route('/star/', methods=['GET'])
def get_one_star(device_name):
  star = mongo.db.stars
  print(device_name)
  s = star.find({'device_name' : device_name})
  if s:
    output = {'ethproto' : s['ethproto'], 'netproto' : s['netproto'],'src_ip':s['src_ip'],'dest_ip':s['dest_ip'],'src_port':s['src_port'],'website':s['website'],'dest_port':s['dest_port'],'device_name':s['device_name'],'confirm':s['confirm']}
  else:
    output = "No such name"
  return jsonify({'result' : output})    




if __name__ == '__main__':
    app.run(debug=True)