from flask import Flask, request, jsonify
import requests
import threading
import time
import logging
import json
from pymongo import MongoClient

logger = logging.getLogger()
client = MongoClient('mongodb://127.0.0.1:27017')
db = client['Kredivo_Dev']
collection = db['Kredivo_Dev']

app = Flask(__name__)

def send_confirm(data):
    time.sleep(1)
    print("Merchant send confirm to Kredivo")
    requests.post(
        url='https://api-sandbox-vn.kredivo.com/checkout/update',
        json=data
    )

@app.route('/push_url', methods=['POST'])
def get_user():
    _data = request.get_json()
    print("amount: ", _data['amount'])
    print("discount_amount: ", (_data['discount_amount']))
    print("disbursed_amount: ", _data['disbursed_amount'])
    print('status: ', _data['trx_status'])
    print("order_id: ", _data['order_id'])
    print('time: ', _data['transaction_time'])
    print('message: ', _data['message'])

    print("Signature_Key: ", _data['signature_key'])
    print("Transaction_ID: ", _data['transaction_id'])
    
    x = threading.Thread(target=send_confirm, args=({
        'signature_key': _data.get('signature_key'),
        'transaction_id': _data.get('transaction_id'),
        "status": "settled"
    },))
    x.start()
    

    return jsonify( {
      "status":"200",
      "message":"OK"
    })

@app.route('/check', methods=['GET'])
def check():
    return jsonify( {
      "status":"OK",
      "message":"Success",
    })

@app.route('/data', methods=['GET'])
def get_order():
    orders = list(collection.find())

    for doc in orders:
        doc['_id'] = str(doc['_id'])

    return jsonify(orders)

if __name__ == '__main__':
    app.run(host = '0.0.0.0',debug = True)




