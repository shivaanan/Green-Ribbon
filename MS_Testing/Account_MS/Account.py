import pyrebase
#from firebase_admin import db   
from flask import Flask, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ 

app = Flask(__name__)

CORS(app)

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
auth = firebase.auth()

app.secret_key = "ESDProject"

db = firebase.database()

# email = "lintao@gmail.com"
# password = "123456"


@app.route("/loginuser", methods=['POST'])
def login_user():
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    print(email)
    print(password)
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user["localId"])
        print("succesful")
        return jsonify({"success": True,
                        "userId": user["localId"]})

    except:
        return jsonify({"success": False})
       

@app.route("/createuser", methods=["POST"])
def create_user():
    data = request.get_json()
    name = data["newName"]
    email = data["newEmail"]
    password = data["newPassword"]

    try:
        user = auth.create_user_with_email_and_password(email, password)

        info = auth.get_account_info(user['idToken'])
        userId = info["users"][0]["localId"]

        addUserNameAndEmail(userId, name, email)

        return jsonify({"success": True})

    except:
        return jsonify({"success": False})
    
# saves user's name and email (saving users particulars)
def addUserNameAndEmail(userId, name, email):
    data = {
        "name" : name,
        "email" : email
    }

    db.child("users").child(userId).set(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
