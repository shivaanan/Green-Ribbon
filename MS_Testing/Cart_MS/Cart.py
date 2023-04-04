from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

# enable CORS
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['CartDB']
collection = db['Cart']

# Get All Cart Items of particular user
@app.route('/get_cart', methods=['GET'])
def getAllProducts():

    data = request.get_json()
    userId = data["userId"]
    
    try:
        cart_items = collection.find({"userId": userId})
        cart_list = []
        print(cart_list)

        for a_item in cart_items:
            a_item['_id'] = str(a_item['_id'])
            cart_list.append(a_item)

        print(cart_list)
        return jsonify({
            'code': 200,
            'cart_list': cart_list
        }), 200    
    except Exception as e:
        return jsonify({
            'code':404,
            'error': str(e)
        }),404


@app.route('/add_to_cart',methods = ['POST'])
def add_to_cart():  
    data = request.get_json()
    buyerID = data["userId"]
    inputQuantity = data["qtyInput"]
    productID = data["productID"]
    product = data['product']

    sellerID = product["sellerID"]
    itemName = product["itemName"]
    price = product['price']
    dateOfPost = product['dateOfPost']
    address = product['address']
    imgURL = product["imgURL"]
    
    # Check if item already in cart
    existing_cart_item = collection.find_one({'buyerID': buyerID, 'productID': productID})
    if existing_cart_item:
        return jsonify({
            'code': 400,
            'message': 'Item already in cart.'
        })
    else:
        collection.insert_one({ 
            "buyerID": buyerID,
            "sellerID": sellerID, 
            "productID": productID,
            "itemName": itemName,
            "inputQuantity": inputQuantity,
            "price": price,
            "dateOfPost": dateOfPost,
            'address': address,
            "imgURL": imgURL
            }
        )
    return jsonify({
        'code': 201,
        "message": "Item has been successfully added to cart"
    }), 201

# Helper function to get all cart items of a single user
def getAllCartItems(user_id):
    cart_items = []
    for item in collection.find({'userId': user_id}):
        cart_items.append(item)
    
    return cart_items

# Delete all items in cart once purchase has been made
@app.route('/delete_from_cart/<user_id>', methods = ['DELETE'])
def delete_from_cart(user_id):
    if len(getAllCartItems(user_id)) > 0:
        collection.delete_many({'userId': user_id})
        return jsonify({
            'code': 200,
            'success': "Cart has been deleted"
        }), 200
    else:
        return jsonify({
            'code': 400,
            'message': 'Cart has is initially empty'
        }), 400
    
@app.route('/delete_one_item/<userId>/<int:productID>', methods = ['DELETE'])
def delete_one_item(userId, productID):
    if len(getAllCartItems(userId)) > 0:
        collection.delete_one({'userId': userId, 'productID': productID})
        return jsonify({
            'code': 200,
            'message': "Item has been deleted from the cart"
        }), 200
    else:
        return jsonify({
            'code': 405,
            'message': "Item was not added into cart initially"
        }), 405

#  port 5002
if __name__ == '__main__':
    app.run(port = 5003, debug = True)