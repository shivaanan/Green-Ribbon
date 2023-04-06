from flask import Flask, request, jsonify
from flask_cors import CORS

import os
import sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

account_URL = environ.get('account_URL') or "http://127.0.0.1:5001"
listing_URL = environ.get('listing_URL') or "http://localhost:5002"
payment_URL = environ.get('payment_URL') or "http://localhost:5005"
cart_URL = environ.get('cart_URL') or "http://127.0.0.1:5003"
order_URL = environ.get('order_URL') or "http://127.0.0.1:5004"
rabbitMQhostname = environ.get('rabbit_host') or "localhost"


@app.route("/buy_item", methods=['POST'])
def buy_item():
    data = request.json
    # shoppingCart = data['dataObj']
    userId = data['userId']
    card_details = data['cardDetails']
    cardHolderName = data['cardName']
    try:
        # cartQuery = {
        #     "buyerID": userId
        # }
        # invoke cartMS to get the cart
        getCartResponse = invoke_http(
            cart_URL + "/get_cart/" + userId, method='GET')
        # print("TEST getCartResponse (START)")
        # print(getCartResponse)
        # print("TEST getCartResponse (END)")
        shoppingCart = getCartResponse['data']["cart_list"]
        # print("TEST shoppingCart (START)")
        # print (shoppingCart)
        # print("TEST shoppingCart (END)")

        manySellerID = []
        for eachItem in shoppingCart:
            product_ID = eachItem['productID']
            productName = eachItem['itemName']

            listing_ms_url = f"{listing_URL}/products/{product_ID}"
            listingResponse = requests.get(listing_ms_url)
            data = listingResponse.json()

            checkProduct = data['data']['product']
            # print("TEST START")
            # # print (eachItem)
            # print(checkProduct)
            # print ("TEST END")

            sellerID = checkProduct['sellerID']
            manySellerID.append(sellerID)

            checkOuantity = checkProduct['quantity']
            currentQuantity = eachItem['inputQuantity']
            # print ("TEST START")
            # print (checkOuantity)
            # print (currentQuantity)
            # print ("TEST END" )
            if currentQuantity > checkOuantity:
                return jsonify({
                    'code': 400,
                    'error': f"Checkout error: {productName} is currently unavailable due to not enough inventory quantity",
                }), 400

        combinedData = {"buyerID": userId, "sellerIDs": manySellerID, "dataObj": shoppingCart, "cardDetails": card_details, "cardName": cardHolderName}
        # print("TEST CD (START)")
        # print(combinedData)
        # print("TEST CD (END)")
        processOrderResult = processOrder(combinedData)
        print("TEST processOrderResult (START)")
        print(processOrderResult)
        print("TEST processOrderResult (END)")


        if processOrderResult['code'] == 201:
            # print(processOrderResult['code'])
            # print(type(processOrderResult['code']))
            # add_to_orders_DataObj = {"buyerID":userId, "paymentStatus":201}
            add_to_orders_result = add_to_orders(processOrderResult['code'], userId)

            error_code = add_to_orders_result["code"]
            print(error_code)
            print (add_to_orders_result)
            print (add_to_orders_result["code"])
            print (type(add_to_orders_result))
            if error_code == 200:
                print("in error code 200   ")
                update_listing_result = update_listing(shoppingCart, error_code)

                if update_listing_result['code'] == 200:
                    delete_cart_result = delete_from_cart(shoppingCart, add_to_orders_result["code"])


        # if processOrderResult['code'] == 201:
        #     add_to_orders_DataObj = {"buyerID":userId, "paymentResult":jsonify(processOrderResult), "paymentStatus":201}
        #     add_to_orders(add_to_orders_DataObj)
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


# ======================== HELPER FUNCTION (START) ========================
def processOrder(products):
    PAYMENT_URL = payment_URL + "/payment"
    payment_result = invoke_http(PAYMENT_URL, method='POST', json=products)

    # print("TEST payment_result (START)")
    # print(payment_result)
    # print("TEST payment_result (END)")

    paymentDescription = payment_result['description']

    buyerID = ""
    sellerIDs = []
    for eachDescription in paymentDescription:
        buyerID = eachDescription['buyerID']
        sellerIDs.append(eachDescription['sellerID'])

    print("ID TEST(START)")
    print(buyerID)
    print(sellerIDs)
    print("ID TEST(END)")

    ACCOUNT_URL = account_URL + "/retrieve_email"

    getBuyerEmail_URL = ACCOUNT_URL + f"/{buyerID}"
    getBuyerEmail = invoke_http(getBuyerEmail_URL, method='GET')
    buyerEmail = getBuyerEmail['data']['email']

    getSellerEmails_set = set()
    for eachSellerID in sellerIDs:
        getSellerEmail_URL = ACCOUNT_URL + f"/{eachSellerID}"
        getSellerEmail = invoke_http(getSellerEmail_URL, method='GET')
        getSellerEmail = getSellerEmail['data']['email']

        getSellerEmails_set.add(getSellerEmail)

    sellerEmails = list(getSellerEmails_set)

    # print("EMAILS (START)")
    # print(sellerEmails)
    # print(buyerEmail)
    # print("EMAILS (END)")


    
    # ========================= AMQP (START) =========================
    code = payment_result["code"]
    message = payment_result

    passMessage = {'message':message,'buyerEmail':buyerEmail, 'sellerEmails':sellerEmails}

    # print("TEST code (START)")
    # print(code)
    # print("TEST code (END)")
    ###################################
    # print("TEST message (START)")
    # print(message)
    # print("TEST message (END)")
    amqp_setup.check_setup()
    json_message = json.dumps(passMessage)

    if code not in range(200, 300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="payment.error", body=json_message, properties=pika.BasicProperties(delivery_mode=2))

        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), payment_result)

        return {
            "code": 500,
            "data": {"payment_result": payment_result},
            "message": payment_result['message']
        }

    else:
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="payment.info", body=json_message)
    # ========================= AMQP (END) =========================

    # Return created Order
    return {
        "code": 201,
        "data": {
            "payment_result": payment_result
        },
        "message": "Payment Successful! Thank you for shopping with us :)"
    }
# ======================== HELPER FUNCTION (END) ========================


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():

    data = request.get_json()
    print(data)
    userId = data["userId"]
    productID = data["productID"]
    qtyInput = data["qtyInput"]
    print("printing product")
    print(productID)

    # use axios to make a post request to listingMS
    # listingMS will return the product with the productID
    result = invoke_http(listing_URL + "/products/" + str(productID), method='GET')
    product = result["data"]["product"]

    # check if the quantity is available
    # if not, return error message
    if (product["quantity"] < int(qtyInput)):
        print("qty less that inventory")

        return jsonify({
            'code': 400,
            "message": "Enter valid quantity!"
        }), 400

    # if yes, invoke cartMS to add to cart
    # cartMS will return the cart
    data = {
        "userId": userId,
        "productID": productID,
        "qtyInput": qtyInput,
        "product": product
    }
    # try:
    cart = invoke_http(cart_URL + "/add_to_cart", method='POST', json=data)

    if (cart["code"] == 200):

        return jsonify({
            'code': 200,
            "message": "Item added to cart!"
        }), 200

    else:
        return jsonify({
            'code': 400,
            "message": "Item already in cart!"
        }), 400


# display user cart on UI
@app.route('/get_cart/<userId>', methods=['GET'])
def get_cart(userId):

    try:
        
        # invoke cartMS to get the cart
        result = invoke_http(cart_URL + "/get_cart/" + userId, method='GET')
        print("printing result")
        print(result)
        cart_list = result["data"]["cart_list"]

        return jsonify({
            'code': 200,
            'message': 'Cart retrieved successfully',
            'data': {
                'cart_list': cart_list
            }
        }), 200

    except:
        return jsonify({
            'code': 400,
            'message': 'Unable to retrieve all cart items'
        }), 400


# # adding to order function
def add_to_orders(paymentStatus, buyerID):

    print("in add to orders")
    print(paymentStatus)
    print(buyerID)
    if paymentStatus == 201:
        getAllItemsURL = cart_URL + "/get_cart/" + buyerID

        
        cartResult = invoke_http(getAllItemsURL, method='GET')
        allCartItems = cartResult["data"]["cart_list"]
        # buyerID = allCartItems[0]["buyerID"]

        addingOrderURL = order_URL + "/add_order"

        data = {
            "cart_list": allCartItems,
            "buyerID": buyerID,
        }
        addingOrderResult = invoke_http(
            addingOrderURL, method='POST', json=data)


        return {
                "code": 200,
                "message": "Order added successfully"
                # "data": {
                #     "cart_list": allCartItems
                # }
                }

    else:
        return {
                "code": 400,
                "message": "Order was not added successfully"
            }



# # updating the listings automatically upon adding to orders
# @app.route('/update_listing', methods = ['PUT'])
def update_listing(allCartItems, addOrdersStatus):
    print("in update listing")
    print(addOrdersStatus)
    print(allCartItems)
    if addOrdersStatus == 200:
        for item in allCartItems:
            productID = item["productID"]
            soldQuantity = item["inputQuantity"]

            updateListingURL = listing_URL + "/update_sold_product_qty"

            updateListingPayload = {
                "productID": productID,
                "soldQuantity": soldQuantity
                }
            
            updateListingResult = invoke_http(
                updateListingURL, method="PUT", json=updateListingPayload)

            if updateListingResult["code"] == 200:
                updatedItem = updateListingResult["data"]["product"]
                if updatedItem["quantity"] <= 0:
                    deleteListingURL = listing_URL + "/remove_product/" + str(productID) 
                    deleteListingResult = invoke_http(deleteListingURL, method="DELETE")


    return {
            "code": 200,
            "message": "Quantity in listing updated successfully"
        }


def delete_from_cart(allCartItems, updateListingStatus):

    if updateListingStatus == 200:
        buyerID = allCartItems[0]["buyerID"]
        deleteFromCartURL = cart_URL + "/delete_from_cart/" + buyerID
        deleteFromCartResult = invoke_http(deleteFromCartURL, method="DELETE")

        return {
                "code": 200,
                "message": "Cart cleared successfully",
                
            }
    else:
        return {
                "code": 400,
                "message": "Cart was not cleared successfully"
            }
        

# deleting 1 item from cart on UI
@app.route('/delete_cart_item/<userId>/<int:productID>', methods=['DELETE'])
def delete_cart_item(userId, productID):

    try:
        result = invoke_http(cart_URL + "/delete_one_item/" + userId + "/" + str(productID), method='DELETE')

        return jsonify({
            'code': 200,
            'message': 'Item deleted successfully'
        })

    except:
        return jsonify({
            'code': 405,
            'message': 'Unable to delete item'
        }), 405


if __name__ == '__main__':
    app.run(port=5200, debug=True, host='0.0.0.0')