import firebase_admin
from firebase_admin import auth
from firebase_admin import db, credentials
from flask import Flask, request, jsonify, session, redirect
from flask_cors import CORS
from os import environ 

app = Flask(__name__)

CORS(app)

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "accounts-c05d0",
  "private_key_id": "fc5a25afeaf48412f91ba69c796a34ef6be6afaf",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCxOCn3tGBg46+i\nh5ZH3anzS0je0GsVnzq8i6eKZstuCJhQ1xWxZhQQjcMMFUvV21Hctv//O2c5gs4a\nMV0DxA8AiYruY2wvnXwsU85BJ2VFguRlhAOZPeXbE962cf5eCs93r+XYF1yBxjwU\nH7nOr46n/8M2UaR/zayNcDVghh+Q1DFhYHUSqQwcBX8vyN3ysRrsKwIHXyadTgbq\nMq2CzSNRskjLJP99UdJ2bqHv+gQrDSJDJWl6kfx9A1TB4BHue0Ftc+5/d1v0KOjs\nZw2HjihtgVL2wP4O378ds6GQOg2scMwyEETZfHn0J3XHDnLEVSqqJKfnwjdBTk6a\n8mycysBDAgMBAAECggEAIXdRtY1Chgl5KWAhaQDbDy6wXCNPlY20MdbNlL1EvUqy\nONHlLtLwBxA+PRHoeEIqe1uzjCdTnvCsqxWXUxa7HobazZnI3FUJFfXdhUBDR5Uo\nPGNpqo6d0Xk3HYz5VBkGhLua0+vVdExTHBnBpN5SOjd6Tc+tGNVmOG9wJQIvA9I9\nnTc8QAmSbys6J2AELJMQlcg5UyJSVpdC4F+IaHXnPrwa4Y4vNn5nIvsGQvR2NGcE\nVSsFf1/2Ph2hypoouOtp1/4BeLsb9sSFWC+viorEgjYC2G79dpp5Gpr7mnoRCB0C\n03b7NzyzXNEFvK/YiJRO1MsRYCJhpWnVV3O/MNzwAQKBgQDo0BCfPCFxE/N8zJj5\ndP3wPGSbUpTJQWUfwTRWDZTL/XtGgYTOJxD5NBCYEGLaFcMg4iYwaRMF8ZNSmM1Q\nSGR9eLu6OOe4XQMQMgDxqsA/rz1Zt3HcivjoIE1eUhtdIezpc1lkFRaJWLYkGEb1\n+u+X3JwxDmdQh2zmx6nG/PjpQwKBgQDC3qgsEabUmpHmM6Yjcc0KZnMutDf3PO5/\nveCJ7g56+h+kgghuIys4N5D7L/VMpqOuYtSjlsLcG33pKvoyRy6z/89XYkRpzGxB\ntihjzQkr02UhfdK7dn/ANryuXJ3fU8gA2k/5yrAv9IvopjllcewfRiE92226tlVZ\n5fXvKxHdAQKBgQC8dvqNvQKhZHI+e+32OxP6rxkOd7qEdVDkdOXmJ5Zl0CxENkMJ\nE6z034XzY4hyXR2Z+BjMJbNFo3sMaTADpqbav6rQpJJIt9rr+F61Q/HfXAABKbSd\nwU6fss6O5U7LhNQhY8RgdYXJ56uC6rg/FkVwnSE/wRY3pXmuFMHGmTDyuwKBgQCR\nu9qhOoI9tWsvcajqEQ16nau+XeEM8XCb7/Cgtnv11GEdsnGDjKGh5UxzziXxMR5w\nKFFGFlWcLqM3YYDDYSC4VLNHcqIfTVYYvpXuLUSSlgGnzmVu9OwNX+Izs+gNQKbu\nnFX7RW4GLykC0G1URKKFsPjjPdsOK5YhKS2Hs/okAQKBgGD50oyUWZlLVcfaH9vh\n0qiSQpfoJeDigJzMJLppBEz9oo9E5M65Nb1f+EnKRymJHKZyc1L1JOofG8QQpvQO\nWgjv/eDQZOoYMje1rrNju8wpmfGA24IB19z5VHghcMCNhb57oQRFxr8DvlNOOBgV\ndAPVETUZr+mL8OWqJ2YO4mI/\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-3tyit@accounts-c05d0.iam.gserviceaccount.com",
  "client_id": "100368083984929806068",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-3tyit%40accounts-c05d0.iam.gserviceaccount.com"
})

# cred = credentials.Certificate('/path/to/firebase-adminsdk.json') # replace with the path to your Firebase Admin SDK JSON file
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://accounts-c05d0-default-rtdb.asia-southeast1.firebasedatabase.app/",
})



app.secret_key = "ESDProject"

db = db.reference()

# # Now you can use auth and db to interact with Firebase services
@app.route("/verify_login", methods=['POST'])
def login_user():
    data = request.get_json()
    email = data["email"]
    input_password = data["password"]

    print(email)

    user = auth.get_user_by_email(email)
    print(user.uid)

    if user:
        print("user exists")
        user_password = db.child("users").child(user.uid).child("password").get()
        
        if input_password == user_password:
            return jsonify(
                {
                    "code": 200,
                    "message": "Login successful",
                    "data" : {
                        "userId": user.uid
                    }
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 400,
                    "message": "Incorrect login details"
                }
            ), 400


@app.route("/create_acct", methods=["POST"])
def create_user():

    data = request.get_json()
    email = data["newEmail"]
    password = data["newPassword"]
    name = data["newName"]

    try:
        user = auth.create_user(
            email = email,
            # email_verified=False,
            password = password,
            # display_name = name,
            # photo_url='http://www.example.com/12345678/photo.png',
            disabled=False)
        print('Sucessfully created new user: {0}'.format(user.uid))

        firebase_admin.db.reference('users').child(user.uid).set({
            'name': name,
            'email': email,
            'password': password
        })  

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
    

# retrieve user email
@app.route("/retrieve_email/<userId>", methods=['GET'])
def retrieve_email(userId):

    email = db.child("users").child(userId).child("email").get()
    print (email)
    if email:
        return jsonify(
            {
                "code": 200,
                "message": "Email retrieved successfully",
                "data": {
                    "email": email
                }
            }), 200
    
    else:
        return jsonify(
            {
                "code": 400,
                "message": "Error occurred when trying to retrieve email"
            }
        ), 400

# retrieve user name
@app.route("/retrieve_name/<userId>", methods=['GET'])
def retrieve_name(userId):

    name = db.child("users").child(userId).child("name").get()
    print (name)
    if name:
        return jsonify(
            {
                "code": 200,
                "message": "Name retrieved successfully",
                "data": {
                    "name": name
                }
            }), 200
    
    else:
        return jsonify(
            {
                "code": 400,
                "message": "Error occurred when trying to retrieve name"
            }
        ), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)