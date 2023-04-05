from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
from os import environ
import requests
from invokes import invoke_http
import pika
import json
import amqp_setup

app = Flask(__name__)
CORS(app)

# URLS used
payment_URL = environ.get('payment_URL') or "http://localhost:5005"
orders_URL = environ.get('orders_URL') or "http://localhost:5004"

#### Endpoints Start ####

# Return an Item (Clicked "Return Item" in Purchased Tab)
@app.route('/return_item', methods=['POST'])
def return_item():
    try:
        data = request.get_json()
        orderID = data['orderID']
        productID = data['productID']
        data['status'] = 'Processing Refund'
        url = f"{orders_URL}/orders/{orderID}/{productID}"
        return_item_result = requests.put(url, json=data)
        checkReturn = return_item_result.json()
        code = checkReturn["code"]
        message = checkReturn["message"]

        if code not in range(200, 300):
            # Inform the error microservice
            print('\n\n-----Publishing the (return item error) message with routing_key=order.error-----')

            # Publish to AMQP Error Queue
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 
            # make message persistent within the matching queues until it is received by some receiver 
            # (the matching queues have to exist and be durable and bound to the exchange)

            # Reply from the invocation is not used;
            # continue even if this invocation fails        
            print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
                code), return_item_result)
            
            # Return error
            return {
                "code": 500,
                "data": {"return_item_result": return_item_result},
                "message": "Return Item failed and sent for error handling."
            }
        
        else:
            # Record New Activity: Request to Return Item made
            print('\n\n-----Publishing the (return item request) message with routing_key=return_item.info-----') ### To be changed

            # invoke_http(activity_log_URL, method="POST", json=order_result)            
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.info", 
                body=message)
            

        return jsonify({'code': 200, 'message': f"Request for return item for Order {orderID} successful"})
    
    except Exception as e:
        return jsonify({'code': 404, 'error': str(e)}), 404
    
# Approval/Rejection of Refund (Seller approved/rejected refund under Sold Tab)
@app.route('/refund_decision', methods=['POST'])
def refund_decision():
    try:
        data = request.get_json()
        orderID = data['orderID']
        productID = data['productID']
        decision = data['decision'] # either "accept" or "reject"

        print("TEST data(START) ")
        print(data)
        print("TEST data(END) ")
        # Get order data from the external API endpoint
        url = f"{orders_URL}/orders/{orderID}/{productID}"
        order_result = requests.get(url)
        order_result = order_result.json()
        print("TEST order(START) ")
        print(order_result)
        print("TEST order(START) ")
        code = order_result["code"]
        order_result = order_result["order"]

        if code not in range(200, 300):
            # Inform the error microservice
            print('\n\n-----Publishing the (return item error) message with routing_key=order.error-----')

            # Publish to AMQP Error Queue ### Should i make this different from the one before
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

            # Reply from the invocation is not used;
            # continue even if this invocation fails        
            print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
                code), order_result)
            
            # Return error
            return {
                "code": 500,
                "data": {"return_item_result": order_result},
                "message": "Return Item failed and sent for error handling."
            }
        else:
            if decision == 'accept':
                shoppingCart = data['dataObj']
                card_details = data['cardDetails']
                cardHolderName = data['cardName']

                # Update order status to "Refunded"
                order_result['status'] = 'Refunded'

                # Send PUT request to update order status
                
                return_result = requests.put(url, json=order_result)
                return_result = return_result.json()
                
                # Processing of Refund via Stripe Wrapper (Uses helper function)
                combinedData = {"dataObj": shoppingCart, "cardDetails": card_details, "cardName": cardHolderName}
                processRefund(combinedData)
                
                # Publish message to RabbitMQ exchange with routing key 'refund.accept'
                return_message = json.dumps(return_result)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.refund.accept",
                                                body=return_message)

                return jsonify({'code': 200,'message': f"Refund accepted for Order {orderID}."})
            

            elif decision == 'reject':
                # Publish message to RabbitMQ exchange with routing key 'refund.reject'
                message = json.dumps(order_result)
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.refund.reject",
                                                body=message)

                # Update order status to "Refund Rejected"
                order_result['status'] = 'Refund Rejected'

                # Send PUT request to update order status
                return_result = requests.put(url, json=order_result)
                return_result = return_result.json()

                return jsonify({'code': 200,'message': f"Refund rejected for Order {orderID}."})

            else:
                return jsonify({'code': 400,'message': f"Invalid decision '{decision}'. Decision should be either 'accept' or 'reject'."})

    except Exception as e:
        return jsonify({'code': 404, 'error': str(e)}), 404

# Helper function to process the refund via Stripe wrapper
def processRefund(products):
    PAYMENT_URL = payment_URL + "/refund"
    refund_result = invoke_http(PAYMENT_URL, method='POST', json=products)

    ## Publish to AMQP
    code = refund_result["code"]
    message = json.dumps(refund_result)
    print(code)
    amqp_setup.check_setup()

    if code not in range(200,300):
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.refund.error", 
            body=message, properties=pika.BasicProperties(delivery_mode = 2))

        print("\nOrder status ({:d}) published to the RabbitMQ Exchange:".format(
            code), refund_result)

        return {
            "code": 500,
            "data": {"payment_result": refund_result},
            "message": "Order creation failure sent for error handling."
        }
    
    else:    
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="return_item.refund.info", 
            body=message)

    # Return Refund Result
    return {
        "code": 201,
        "data": {
            "payment_result": refund_result
        },
        "message": "Payment Successful! Thank you for shopping with us :)"
    }

if __name__ == '__main__':
    app.run(port=5300, debug=True)