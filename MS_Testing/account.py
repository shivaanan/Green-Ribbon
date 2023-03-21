import pyrebase
#from firebase_admin import db   
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ 

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/book'
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') # this line is to make it dynamic not just localhost
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
def connect(): 
    firebaseConfig = {
        "apiKey": "AIzaSyAIKcr2frkfzrTQ6-tqOnCtAdmSpHbgr_s",
        "authDomain": "accounts-c05d0.firebaseapp.com",
        "databaseURL": "https://accounts-c05d0-default-rtdb.asia-southeast1.firebasedatabase.app/",
        "projectId": "accounts-c05d0",
        "storageBucket": "accounts-c05d0.appspot.com",
        "messagingSenderId": "227849453678",
        "appId": "1:227849453678:web:3dde5e550b809fbc1d667f",
        "measurementId": "G-V2EQLKY1JV"
    }

    firebase = pyrebase.initialize_app(firebaseConfig)
    
    return firebase.database() 

db = connect() 
# CORS(app)

data = {
    "users" : {
    "1234" : {
      "userid" : "1234",
      "email" : "lintao@gmail.com",
      "username" : "lintao",
      "password" : "000000"
    }, 
    "0000" : {
      "userid" : "0000",
      "email" : "martin@gmail.com",
      "username" : "martin",
      "password" : "123456"
    } 
  }
}
db.set(data)
# display = db.child("users").order_by_child("userid").equal_to("1234").get()
# print(display)
# snapshot = db.child("users").order_by_child('userid').equal_to("1234").get()
# for key in snapshot:
#     print(key)

@app.route("/createuser", methods=['POST'])
def create_user() : 
    data = request.get_json() 
    userid = data["userid"]
    try: 
        db.child("users").child(userid).set(data)
    except: 
        return jsonify(
            {
                "code": 500, 
                "data": data, 
                "message": "An error occurred creating the account"
            }
        ), 500 
    return jsonify ( 
        {
            "code": 201, 
            "data": data, 
            "message": "Account successfully created."
        }
    ), 201 


@app.route("/loginuser", methods=['POST'])
def login_user():
    data = request.get_json()
    userid = data["userid"]
    try:
        userobj = db.child("users").order_by_child("userid").equal_to(userid).get()
        userobj = userobj.val()
      
        if userobj and userobj[userid]['username'] == data['username'] and userobj[userid]['password'] == data['password']:
            return jsonify(
                {
                    "code": 200,
                    "data": userid,
                    "message": "Login successful."
                }
            ), 200
        else:
            return jsonify(
                {
                    "code": 400,
                    "data": userid,
                    "message": "Invalid username or password."
                }
            ), 400
    except:
        return jsonify(
            {
                "code": 400,
                "data": data,
                "message": "An error occurred while trying to log in."
            }
        ), 400
       

@app.route("/getallusers", methods=["GET"])
def getalluser(): 
    try: 
        data = db.child("users").get()
        data = data.val()
        num = len(data)
        num = str(num)
        if data == []:
            return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "data": data
                    }, 
                    "message": 'No users in database'
                }
            ), 400 
    except: 
        return jsonify(
            {
                "code": 400, 
                "data": {
                    "data": data 
                }, 
                "message": "Error occured when trying to get all users"
            }
        ), 400 
    return jsonify( 
        {
            "code": 200,
            "data": data,
            "message": "Successfully returned " + num + " users"
        }
    ), 200 


@app.route("/getbyuseremail/<string:email>", methods=['GET'])
def getbyuseremail(email):
    try: 
        email = email.lower()
        userobj = db.child("users").order_by_child("email").equal_to(email).get()
        userobj = userobj.val() 
        if userobj == []: 
            return jsonify(
                {
                    "code": 400, 
                    "data": {
                        "email" : email  
                    },
                    "message": "User not found"
                }
            ), 400 
    except: 
        return jsonify(
            {
                "code": 400,
                "data": { 
                    "userid" : email 
                }, 
                "message": "Error occured when trying to get user"
            }
        ), 400
    return jsonify(
        {
            "code": 200,
            "data": userobj,
        }
    ), 200


@app.route("/getbyuserid/<string:userid>", methods=['GET'])
def getbyuserid(userid):
    try: 
       userobj = db.child("users").order_by_child("userid").equal_to(userid).get()
       userobj = userobj.val()
       if userobj == [] : 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userid" : userid
                },
                "message": "User not found"
            }
        ), 400 
    except: 
        return jsonify(
            {
                "code": 400,
                "data": {
                    "userid" : userid 
                },
                "message": "Error occurred when trying to get user"
            }
        ), 400
    return jsonify(
        {
            "code": 200,
            "data": userobj
        }
    ), 200 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
