from flask import request
from flask import jsonify
from flask import Flask
from flask_cors import CORS,cross_origin

app = Flask(__name__)

@app.route('/hello', methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def hello():
    message = request.get_json(force=True)
    name = message['name']
    response = {
        'greeting': 'Hello, ' + name
    }
    return jsonify(response)