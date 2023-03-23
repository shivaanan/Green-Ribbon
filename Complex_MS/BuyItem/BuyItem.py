from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import amqp_setup
import pika
import json

app = Flask(__name__)
CORS(app)

listing_URL = environ.get('listing_URL') or "http://localhost:5001/products" 
payment_URL = environ.get('payment_URL') or "http://localhost:5002//create-checkout-session" 
cart_URL = environ.get('cart_URL') or "http://localhost:5003/add_to_cart" 


if __name__ == '__main__':
    app.run( port=5100, debug=True)