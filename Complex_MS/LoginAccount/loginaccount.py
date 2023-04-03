import firebase 
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

# Check if user exist 
# def ifexists(email): 
#     getallURL = accountMSURL + "/getallusers"
#     result = invoke_http(getallURL, method='GET')
#     users = result['data']
#     error = []
#     if email in users: 
#         error.append('user')
#     if users == {} : 
#         return error 
#     return error 

# Add new user to database
@app.route("/create_acct", methods=['POST'])
def create_account(): 
    data = request.get_json()

    try : 

        createAccountURL = accountMSURL + "/createuser"
        result = invoke_http(createAccountURL, method='POST', json=data)

        return jsonify(
            {
                "code": 201, 
                "message": "Account created successfully"
            }
        ), 201 
    except Exception as e: 
        return jsonify(
            {
                "code": 400,
                "message": "Error occurred when trying to create user" 
            }
        ), 400

# Verify user login 
@app.route("/verifylogin", methods=['POST']) 
def verifylogin(): 
    #get login post request 
    data = request.get_json()
    email = data['email'].lower() 
    if email == "":
        return jsonify (
            {
                "code": 400,
                "data": None,
                "message": "Please key in the proper login details"
            }
    ), 400 
    try: 
        accountURL = accountMSURL + "/loginuser" 
        result = invoke_http(accountURL, method='POST', json=data)
        status = result['success']
        if status == False: 
            amqpmessage = "Error retrieving account, incorrect login details"
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", body=amqpmessage)
            return jsonify( 
                {
                    "code": 400, 
                    "data": result, 
                    "message": "Incorrect login details"
                }
        ), 400 
        else : 
            amqpmessage = "Account retrieved successfully"
            amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.info", body=amqpmessage)
            user = result['userId']
            return jsonify(
                    {
                        "code": 201,
                        "data": user,
                        "message": "Login successful"
                    }
                ), 201
    
    except:
        amqpmessage = "Error retrieving account, incorrect login details"
        amqp_setup.channel.basic_publish(exchange=amqp_setup.exchangename, routing_key="login.error", body=amqpmessage)
        return jsonify(
            {
                "code": 400,
                "data": result,
                "message": "Incorrect login details or password."
            }
        ), 400

# 4. Get location data 
@app.route('/calculatedistance', methods=['GET'])
def get_distance():
    try:
        destaddresses = {}
        listingURL = listingMSURL + "/products"   
        result = invoke_http(listingURL, method='GET')
        for listing in result : 
            destaddresses[listing["productID"]] = listing["address"]
        print(destaddresses)

        locresponse = invoke_http(locationMSURL + "/location", method='POST')
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

        return jsonify(distances)
    except :
         return jsonify(
            {
                "code": 400,
                "data": response,
                "message": "Failed to calculate distance"
            }
        ), 400


if __name__ == '__main__':
    CORS(app)
    app.run(host='0.0.0.0', port=5100, debug=True)