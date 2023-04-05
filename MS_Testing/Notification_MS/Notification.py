#!/usr/bin/env python3

import os
import json
import amqp_setup
import pika

from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from os import environ ###
from dotenv import load_dotenv

load_dotenv()
SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']

app = Flask(__name__)


monitorBindingKey='#'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    paymentQueue = 'Payment'
    
    amqp_setup.channel.basic_consume(queue=paymentQueue, on_message_callback=paymentNotification, auto_ack=True)

    returnQueue = 'Return_Payment'
    
    amqp_setup.channel.basic_consume(queue=returnQueue, on_message_callback=refundNotification, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 

def paymentNotification(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    try:
        processOrderLog(json.loads(body))
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an order log:")
    print(order)
    send_payment_notification(order) # Send payment status to users 
    

def send_payment_notification(data):
    # code = data.get('code', 0)
    # message = data.get('message', '')

    # # Extract email address from data (assuming it's included)
    # email = data.get('email', '')

    # print("Test data (START)")
    # print(data)
    # print("Test data (END)")
    # code = data['code']
    try:
        message = data['message']
        paymentStatus = message['paymentStatus']

        buyerEmail = data['buyerEmail']
        seller_Emails = data['sellerEmails']

        if paymentStatus == 'Payment_Successful':
            subjectBuyer = "Purchase Successful"
            messageBuyer = f"You have purchased {message['purchaseSummary']['checkoutDescription']}. Total amount is ${message['purchaseSummary']['totalAmount']}USD"

            subjectSeller = "Purchase Successful"
            messageSeller = f"We are excited to inform you that your item has been successfully sold on our platform! Congratulations on making a sale, and we appreciate your trust in using our services."

        else:
            return {"error": "Invalid status code"}, 400

        # Send email using SendGrid
        send_email(buyerEmail, subjectBuyer, messageBuyer)

        for eachSellerEmail in seller_Emails:
            send_email(eachSellerEmail, subjectSeller, messageSeller)

        return {
            "code": 201,
            "message": "Email sent"
        }
    
    except:
        return {
            "code": 400,
            "message": "Email fail to send"
        }

def refundNotification(channel, method, properties, body): # required signature for the callback; no return
    # print("TEST")
    # print(body)
    # print("TEST(END)")
    print("\nReceived an order log by " + __file__)
    try:
        processRefundLog(json.loads(body))
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
    print() # print a new line feed

def processRefundLog(order):
    print("Recording an order log:")
    print(order)
    send_refund_notification(order) # Send payment status to users 
    

def send_refund_notification(data):

    # code = data.get('code', 0)
    # message = data.get('message', '')

    # # Extract email address from data (assuming it's included)
    # email = data.get('email', '')

    # print("Test data (START)")
    # print(data)
    # print("Test data (END)")

    # code = data['code']
    try:
        refundStatus = data['message']['code']

        buyerEmail=data['buyerEmail']
        sellerEmail=data['sellerEmail']

        if refundStatus == 201:
            orderID = data['message']['description'][0]['orderID']
            productID = data['message']['description'][0]['productID']

            subjectBuyer = "Refund Successful"
            messageBuyer = f"Your purchase of Product {productID} from Order {orderID} has been successfully refunded."

            subjectSeller = "Refund Successful"
            messageSeller = f"We would like to inform you that you have successfully refunded Product {productID} from Order {orderID} to the Buyer."

        else:
            return {"error": "Invalid status code"}, 400

        # Send email using SendGrid
        send_email(buyerEmail, subjectBuyer, messageBuyer)
        send_email(sellerEmail, subjectSeller, messageSeller)
        return {
            "code": 201,
            "message": "Email sent"
        }, 201
    
    except:
        return {
            "code": 400,
            "message": "Email fail to send"
        }

def send_email(to_email, subject, content):
    message = Mail(
        from_email="lintao199@gmail.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        # print("TEST (START)")
        # print(sg)
        # print("BREAK")
        # print(response)
        # print("TEST (END)")

        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print("Error sending email")
    print() # print a new line feed


if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()


# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5006, debug=True)
