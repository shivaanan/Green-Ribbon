import os
from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, firestore

from datetime import datetime
import json


app = Flask(__name__)
# Firestore
cred = credentials.Certificate("api/key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


@app.route('/orders', methods=['GET'])
def get_orders():
    orders = []
    for order in db.collection('orders').stream():
        orders.append(order.to_dict())
    return jsonify(orders)

@app.route('/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = db.collection('orders').document(order_id).get()
    return jsonify(order.to_dict())

@app.route('/orders', methods=['POST'])
def create_order():
    order = request.json
    db.collection('orders').document().set(order)
    return jsonify({'message': 'Order created successfully!'})

@app.route('/orders/<order_id>', methods=['PUT'])
def update_order(order_id):
    order = request.json
    db.collection('orders').document(order_id).update(order)
    return jsonify({'message': 'Order updated successfully!'})

@app.route('/orders/<order_id>', methods=['DELETE'])
def delete_order(order_id):
    db.collection('orders').document(order_id).delete()
    return jsonify({'message': 'Order deleted successfully!'})

# Run
if __name__ == '__main__':
    app.run()