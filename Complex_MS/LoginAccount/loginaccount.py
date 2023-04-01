import firebase 
from flask import Flask, request, jsonify 
from flask_cors import CORS 
from invokes import invoke_http
import pika 
import os 
import json
import requests
from os import environ 

# connect to rabbitMQ 
# rabbitMQhostname = os.environ['rabbit_host'] or "localhost"
# port = 5672
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(
#         host=rabbitMQhostname, port=port, 
#         heartbeat=3600, blocked_connection_timeout=3600,
#     )
# ) 
# channel = connection.channel()
# exchangename = "order_topic"
# exchangetype = "topic"

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

accountMSURL = environ.get('account_URL') or 'http://localhost:5200'
locationMSURL = environ.get('location_URL') or 'http://localhost:8080'
listingMSURL = environ.get('listing_URL') or 'http://localhost:5001'

# 1. Check if user exist in firebase 
def ifexists(email): 
    getallURL = accountMSURL + "/getallusers"
    result = invoke_http(getallURL, method='GET')
    users = result['data']
    error = []
    if users == {} : 
        return error 
    if email in users: 
        error.append('user')
    return error 

# 2. Add new user to database
@app.route("/createacc", methods=['POST'])
def create_account(): 
    data = request.get_json()
    print(data)
    data['newEmail'] = data['newEmail'].lower() 
    email = data['newEmail']
    try : 
        ifexists(email)
        errors = ifexists(email)
        message = "Email already exists"
        if len(errors) > 0: 
            #amqpmsg = 'Tried to create account with Email: ' + email + "but ran into errors: " + message
            #channel.basic_publish(exchange=exchangename, routing_key="", body=amqpmsg, properties=pika.BasicProperties(delivery_mode=2)) 
            return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "email": email 
                    }, 
                    "message": message 
                }
            ), 400 
        accountURL = accountMSURL + "/createuser"
        result = invoke_http(accountURL, method='POST', json=data)
        status = result['success']
        if status == False : 
            return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "result": result 
                    }, 
                    "message": message 
                }
            ), 400 
        else : 
            message = "Account created successfully"
            #channel.basic_publish(exchange=exchangename, routing_key="", body=message)
            return jsonify(
                {
                    "code": 201, 
                    "data": result,
                    "message": "Account created successfully"
                }
            ), 201 
    except : 
        return jsonify(
            {
                "code": 400,
                "data": email,
                "message": "Error creating account."
            }
        ), 400

# 3. Verify user login 

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
            return jsonify( 
                {
                    "code": 400, 
                    "data": result, 
                    "message": "Incorrect login details"
                }
        ), 400 
        else : 
            user = result['userId']
            return jsonify(
                    {
                        "code": 201,
                        "data": user,
                        "message": "Login successful"
                    }
                ), 201
    
    except:
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
    app.run(host='0.0.0.0', port=5300, debug=True)