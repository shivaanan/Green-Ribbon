#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import json
import os
import requests

import amqp_setup

monitorBindingKey='#'

def receiveOrderLog():
    amqp_setup.check_setup()
        
    queue_name = 'Activity_Log'
    
    amqp_setup.channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    amqp_setup.channel.start_consuming() # an implicit loop waiting to receive messages; 

def callback(channel, method, properties, body): # required signature for the callback; no return
    print("\nReceived an order log by " + __file__)
    processOrderLog(json.loads(body))
    print() # print a new line feed

def processOrderLog(order):
    print("Recording an order log:")
    # send_notification(order) # Send payment status to users 
    print(order)

# ============================== PAYMENT EMAIL (START) ==============================
# def send_notification(data):
#     try:
#         response = requests.post("http://127.0.0.1:5006/paymentNotification", json=data)
#         response.raise_for_status()
#     except requests.exceptions.RequestException as e:
#         print("Error sending notification:", e)
# ============================== PAYMENT EMAIL (END) ==============================

if __name__ == "__main__":  # execute this program only if it is run as a script (not by 'import')
    print("\nThis is " + os.path.basename(__file__), end='')
    print(": monitoring routing key '{}' in exchange '{}' ...".format(monitorBindingKey, amqp_setup.exchangename))
    receiveOrderLog()
