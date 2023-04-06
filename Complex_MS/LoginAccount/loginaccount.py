# import firebase 
from flask import Flask, request, jsonify 
from flask_cors import CORS 
from invokes import invoke_http
import pika 
import os 
import json
import requests
import amqp_setup
from os import environ 

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

accountMSURL = environ.get('account_URL') or 'http://localhost:5001'
locationMSURL = environ.get('location_URL') or 'http://localhost:8080'
listingMSURL = environ.get('listing_URL') or 'http://localhost:5002'


# Add new user to database
@app.route("/create_acct", methods=['POST'])
def create_account(): 
    data = request.get_json()

    try : 

        createAccountURL = accountMSURL + "/create_acct"
        result = invoke_http(createAccountURL, method='POST', json=data)

        return jsonify(
            {
                "code": 201, 
                "message": "Account created successfully"
            }
        ), 201 
    except: 
        return jsonify(
            {
                "code": 400,
                "message": "Error occurred when trying to create user" 
            }
        ), 400

# Verify user login 
@app.route("/verify_login", methods=['POST']) 
def verifylogin(): 
    #get login post request 
    data = request.get_json()

    try: 
        accountURL = accountMSURL + "/verify_login" 
        result = invoke_http(accountURL, method='POST', json=data)

        amqpmessage = "Account retrieved successfully"
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.info", body=amqpmessage)

        data = result['data']
        return jsonify(
                {
                    "code": 200,
                    "data": data,
                    "message": "Login successful"
                }
            ), 200
    
    except:
        amqpmessage = "Error retrieving account, incorrect login details"
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", body=amqpmessage)

        return jsonify(
            {
                "code": 400,
                "message": "Incorrect login details"
            }
        ), 400

# 4. Get location data 
@app.route('/calculatedistance', methods=['GET'])
def get_distance():
    try:
        destaddresses = {}
        listingURL = listingMSURL + "/products"   
        result = invoke_http(listingURL, method='GET')
        print(result)
        for listing in result["data"]["products"]: 
            destaddresses[listing["productID"]] = listing["address"]
        print(destaddresses)
        print(locationMSURL + "/location")
        locresponse = invoke_http(locationMSURL + "/location", method='GET')
        print(locresponse)
        if locresponse == []: 
            amqpmessage = "Error getting user location"
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="location.error", body=amqpmessage,properties=pika.BasicProperties(delivery_mode=2))

        distances = {}
        for destaddress in destaddresses:
            
            #print(destaddresses[destaddress])
            api_key = "AIzaSyCItPqAhCSJVc13yxvnZoHb7SyTajxJWJ8"
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={destaddresses[destaddress]}&key={api_key}"
            response = requests.get(url)
            data = response.json()

            if data['status'] == 'OK':
        
                destlocation = data['results'][0]['geometry']['location']
                dest_lat = destlocation['lat']
                dest_lng = destlocation['lng']
                
                origin = f"{locresponse['lat']},{locresponse['lng']}"
                destination = f"{dest_lat},{dest_lng}"
                url = f"https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={origin}&destinations={destination}&key={api_key}"
                response = requests.get(url)
                data = response.json()

                distance = data['rows'][0]['elements'][0]['distance']['value'] / 1000  # Convert from meters to kilometers
                distances[destaddress] = round(distance, 1) 
            else:
                distances.append(-1)  # Set distance to -1 if Geocoding API returns an error
                amqpmessage = "Error calculating distance"
                amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="location.error", body=amqpmessage,properties=pika.BasicProperties(delivery_mode=2))

        return jsonify({
            "code": 200,
            "data": {
                "distances": distances
            },
            "message": "Distance calculated successfully"
        })
    
    except :
         return jsonify(
            {
                "code": 400,
                "message": "Failed to calculate distance"
            }
        ), 400

# Get all products
@app.route("/products", methods=['GET'])
def get_all_products(): 

    try : 

        productListingURL = listingMSURL + "/products"
        result = invoke_http(productListingURL, method='GET')

        data = result["data"]

        return jsonify(
            {
                    "code": 200,
                    "data": data,
                    "message": "Retrieved all products"
            }
        ), 200
     
    except: 

        return jsonify(
            {
                "code": 400,
                "message": "Unable to retrieve all products"
            }
        ), 400
    
if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5100, debug=True)