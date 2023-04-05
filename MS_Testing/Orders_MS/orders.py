import os
from flask import Flask, request, jsonify
import datetime
import json

from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

# enable CORS
CORS(app)

# Connect to MongoDB
client = MongoClient(
    'mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['OrdersDB']
collection = db['Orders']


# Get all Orders Made by userid parsed in via URL
# Used in "Purchased" Tab of Profile
@app.route('/purchased/<userID>', methods=['GET']) #
def getAllPurchased(userID): # 
    try:
        orders = list(collection.find({'buyerID': userID})) # This should be modified to check if buyer/seller is userID
        order_list = []
        for order in orders:
            order_dict = {
                'code': 200,
                'orderID': order["orderID"],
                'buyerID': order["buyerID"],
                'sellerID': order["sellerID"],
                'productID': order["productID"],
                'itemName': order['itemName'],
                'quantity': order['quantity'],
                'price': order['price'],
                'dateOfOrder': order['dateOfOrder'],
                'imgURL': order["imgURL"],
                'dateOfPost': order['dateOfPost'],
                'address': order['address'],
                'status' : order["status"]
            }
            order_list.append(order_dict)
        return jsonify(order_list)
    except Exception as e:
        return jsonify({'code': 404, 'error': str(e)}), 404
    
# Get all Orders SOLD by userid parsed in via URL
# Used in "Sold" Tab of Profile
@app.route('/sold/<userID>', methods=['GET']) #
def getAllSold(userID): # 
    try:
        orders = list(collection.find({'sellerID': userID}))
        order_list = []
        for order in orders:
            order_dict = {
                'code': 200,
                'orderID': order["orderID"],
                'buyerID': order["buyerID"],
                'sellerID': order["sellerID"],
                'productID': order["productID"],
                'itemName': order['itemName'],
                'quantity': order['quantity'],
                'price': order['price'],
                'dateOfOrder': order['dateOfOrder'],
                'imgURL': order["imgURL"],
                'dateOfPost': order['dateOfPost'],
                'address': order['address'],
                'status' : order["status"]
            }
            order_list.append(order_dict)
        return jsonify(order_list)
    except Exception as e:
        return jsonify({'code': 404, 'error': str(e)}), 404

# Look at 1 Order
# Use case: When clicking into an order?
@app.route('/orders/<int:orderID>/<int:productID>', methods=['GET'])
def getOrderByID(orderID, productID):
    order = collection.find_one({'orderID': orderID, 'productID':productID})
    if order:
        order_dict = {
            'orderID': order["orderID"],
            'buyerID': order["buyerID"],
            'sellerID': order["sellerID"],
            'productID': order["productID"],
            'itemName': order['itemName'],
            'quantity': order['quantity'],
            'price': order['price'],
            'dateOfOrder': order['dateOfOrder'],
            'imgURL': order["imgURL"],
            'dateOfPost': order['dateOfPost'],
            'address': order['address'],
            'status' : order["status"]
        }
        return jsonify({'code':200, 'order': order_dict})
    else:
        return jsonify(
            {
                'code': 404,
                'error': 'Order not found (getOrderbyID)'
            }
        ), 404

# Make an Order 
# Use Case: in Buy Item Complex MS, edit item in ListingsMS and add it to Order
@app.route('/add_order', methods=['POST'])
def add_order():
    try:
        # Get the next order ID from the database
        orderID =  get_next_sequence_value("order_id")
        
        # Get the order details from the request payload
        order_data = request.get_json() 
        cart = order_data["cart_list"] # If theres more than one item passed in

        buyerID = order_data["buyerID"]
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%d-%m-%Y")
        dateOfOrder = formatted_date 
        status = "Completed"

        # Add the order(s) to the database
        for data in cart:
            itemName = data["itemName"]
            sellerID = data["sellerID"]
            productID = data["productID"]
            quantity = data['inputQuantity']
            price = data['price']
            imgURL = data["imgURL"]
            dateOfPost = data["dateOfPost"]
            address = data["address"]

            collection.insert_one({
                'orderID': orderID,
                'buyerID': buyerID,
                'sellerID': sellerID,
                'productID':productID,
                'itemName': itemName,
                'quantity': quantity,
                'price': price,
                'dateOfOrder': dateOfOrder,
                'imgURL': imgURL,
                'dateOfPost':dateOfPost,
                'address':address,
                "status": status
            })

        # Return a success response
        return jsonify({'code':201, 'message': 'Order added successfully.'}), 201

    except Exception as e:
        # Return an error response if there was a problem adding the order to the database
        return jsonify({'error': str(e)}), 500

def get_next_sequence_value(sequence_name):
    counter = db.counters
    sequence_value = counter.find_one_and_update(
        {"_id": sequence_name}, {"$inc": {"seq": 1}})
    return sequence_value['seq']

# Update the Status of an Order
# Use case: Anything to do with refunding
@app.route('/orders/<int:orderID>/<int:productID>', methods=['PUT'])
def update_order_status(orderID, productID):
    try:
        data = request.get_json()
        newStatus = data['status']

        result = collection.update_one({"orderID": orderID, "productID":productID}, {"$set": {"status": newStatus}})

        if result.modified_count == 1:
            return jsonify({'code':200, 'message': f"Order {orderID}, Product {productID} updated successfully","orderID":orderID,"productID":productID})
        else:
            return jsonify({'code':404, 'message': f"No order with ID {orderID} and Product {productID} found"}), 404
    except Exception as e:
        return jsonify({'code': 500, 'error': str(e)}), 500

# Run
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)