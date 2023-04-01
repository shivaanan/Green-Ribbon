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
payment_URL = environ.get(
    'payment_URL') or "http://localhost:5002/create_payment_intent"
cart_URL = environ.get('cart_URL') or "http://127.0.0.1:5003"


@app.route("/buy_item", methods=['POST'])
def buy_item():
    if request.is_json:
        shoppingCart = request.json
        try:
            # product_ids = data['productID']

            # frontend_base_url = data.get('frontend_base_url', 'http://localhost:3000')
            # Fetch the product information from the Listing Micro Service
            # Replace with the actual URL of your Listing Micro Service
            print("TEST shoppingCart (START)")
            print(shoppingCart)
            print("TEST shoppingCart (END)")
            for eachItem in shoppingCart:
                product_ID = eachItem['productID']
                productName = eachItem['itemName']
                listing_ms_url = f"{listing_URL}/{product_ID}"

                listingResponse = requests.get(listing_ms_url)
                checkProduct = listingResponse.json()
                # print("TEST START")
                # print(eachItem)
                # print(listingResponse.json())
                # print("TEST END")

                checkQuantity = checkProduct['quantity']
                currentQuantity = eachItem['inputQuantity']
                # print("TEST START")
                # print(checkQuantity)
                # print(currentQuantity)
                # print("TEST END")

                if currentQuantity > checkQuantity:
                    return jsonify({
                        'code': 404,
                        'error': f"Checkout error: {productName} is currently unavailable due to not enough inventory quantity"
                    }), 404

            processOrderResult = processOrder(shoppingCart)
            print("TEST processOrderResult (START)")
            print(processOrderResult)
            print("TEST processOrderResult (END)")
            
            return jsonify(processOrderResult), processOrderResult["code"]

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

# ======================== HELPER FUNCTION ========================
def processOrder(products):
    payment_result = invoke_http(payment_URL, method='POST', json=products)

    # Add AMQP HERE

    # Return created Order
    return {
        "code": 201,
        "data": {
            "message": "Payment Intent created Successfully by STRIPE",
            "payment_result": payment_result
        }
    }
# ======================== HELPER FUNCTION ========================

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    data = request.get_json()
    print(data)
    userId = data["userId"]
    productID = data["productId"]
    qtyInput = int(data["qtyInput"])
    print("printing product")
    print(productID)

    # use axios to make a post request to listingMS
    # listingMS will return the product with the productID
    product = invoke_http(listing_URL + "/" + str(productID), method='GET')
    print(product)
    # check if the quantity is available
    # if not, return error message
    if (product["quantity"] < qtyInput):
        print("qty less that inventory")
        return jsonify(
            {
                'success': False,
                'error': 'Enter valid quantity!'
            }
        )

    # if yes, invoke cartMS to add to cart
    # cartMS will return the cart
    data = {
        "userId": userId,
        "productID": productID,
        "qtyInput": qtyInput,
        "product": product
    }
    cart = invoke_http(cart_URL + "/add_to_cart", method='POST', json=data)

    if (cart["success"]):
        return jsonify(
            {
                'success': True
            }
        ), 200

    return jsonify({
        'success': False,
        "error": "Item already in cart"
    })


@app.route('/get_cart/<userId>', methods=['GET'])
def get_cart(userId):

    # data = request.get_json()
    data = {
        "userId": userId
    }
    # invoke cartMS to get the cart
    cart = invoke_http(cart_URL + "/get_cart", method='GET', json=data)

    cart_list = cart["cart_list"]

    return jsonify(cart_list)


@app.route("/get_cart_count/<userId>", methods=['GET'])
def get_cart_count(userId):
    # data = request.get_json();
    # userId = data["userId"]

    cart = get_cart_helper_func(userId)
    count = len(cart["cart_list"])

    print(count)
    return jsonify({
        "cart_count": count})

# helper function to get cart


def get_cart_helper_func(userId):
    data = {
        "userId": userId
    }

    # invoke cartMS to get the cart
    cart = invoke_http(cart_URL + "/get_cart", method='GET', json=data)

    return cart


if __name__ == '__main__':
    app.run(port=5100, debug=True)
