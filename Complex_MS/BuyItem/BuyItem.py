from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json

app = Flask(__name__)
CORS(app)

listing_URL = environ.get('listing_URL') or "http://localhost:5001/products"
payment_URL = environ.get('payment_URL') or "http://localhost:5002/create_payment_intent"
cart_URL = environ.get('cart_URL') or "http://localhost:5003/add_to_cart"


@app.route("/buy_item", methods=['POST'])
def buy_item():
    if request.is_json:
        data = request.json
        try:
            product_id = data['product_id']

            # frontend_base_url = data.get('frontend_base_url', 'http://localhost:3000')
            # Fetch the product information from the Listing Micro Service
            # Replace with the actual URL of your Listing Micro Service
            listing_ms_url = f"{listing_URL}/{product_id}"
            response = requests.get(listing_ms_url)

            products = response.json()
            print(products)
            if response.status_code != 200:
                return jsonify({
                    'code': 404,
                    'error': 'Product not found'
                }), 404

            result = processOrder(products)

            return jsonify(result), result["code"]

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + \
                fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "place_order.py internal error: " + ex_str
            }), 500
        
    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400


def processOrder(products):
    payment_result = invoke_http(payment_URL, method='POST', json=products)

    # Return created Order
    return {
        "code": 201,
        "data": {
            "payment_result": payment_result
        }
    }

@app.route('/add_to_cart', methods=['GET'])
def add_to_cart():

    # check qty from listingMS
    data = request.get_json()
    productID = data["productID"]
    input_quantity = data["quantity"]

    # use axios to make a post request to listingMS
    # listingMS will return the product with the productID
    product = invoke_http(listing_URL + "/" + str(productID), method='GET')

    # check if the quantity is available
    # if not, return error message

    if product["quantity"] < input_quantity:
        return jsonify(
            {
                'code': 404,
                'error': 'Not enough quantity'
            }
        ), 404

    # if yes, invoke cartMS to add to cart
    # cartMS will return the cart
    cart = invoke_http(cart_URL, method='POST', json=data)

    



if __name__ == '__main__':
    app.run(port=5100, debug=True)
