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

cart = {}

# # Get 1 Product
# @app.route('/products/<int:productID>', methods=['GET'])
def getProductByID(productID):
    product = collection.find_one({'productID': productID})
    # if product:
    #     product_dict = {
    #         'productID': product["productID"], 
    #         'itemName': product['itemName'], 
    #         'quantity': product['quantity'],
    #         'price': product['price'], 
    #         'dateOfPost': product['dateOfPost'], 
    #         'availability': product['availability'],
    #         # 'location': product['location'],
    #         'imgURL': product["imgURL"]
    #     }
        # return jsonify(product_dict)
    return product

#     else:
#         return jsonify(
#             {
#                 'code': 404,
#                 'error': 'Product not found'
#             }
#         ), 404

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
            a_item['_id'] = str(a_item['_id'])  # convert ObjectId to string
            cart_list.append(a_item)

        print(cart_list)
        return jsonify({
            'code': 200,
            'cart_list': cart_list})
    
    except Exception as e:
        return jsonify({'code':404,'error': str(e)}),404
    


@app.route('/add_to_cart',methods = ['POST'])
def add_to_cart():  
    data = request.get_json()
    userId = data["userId"]
    input_quantity = data["qtyInput"]
    productID = data["productID"]
    product = data['product']

    itemName = product["itemName"]
    quantity = product['quantity']
    price = product['price']
    dateOfPost = product['dateOfPost']
    availability = product['availability']
    # location = data['location']
    imgURL = product["imgURL"]
    
    # Check if item already in cart
    existing_cart_item = collection.find_one({'userId': userId, 'productID': productID})
    if existing_cart_item:
        return jsonify({'success': False, 'message': 'Item already in cart.'})
    else:
        collection.insert_one({ 
            "userId": userId, 
            "productID": productID,
            "itemName": itemName,
            "inputQuantity": input_quantity,
            "price": price,
            "dateOfPost": dateOfPost,
            # 'location': location,
            "imgURL": imgURL
            }
        )

    return jsonify({"success": True}), 200

# Helper function to get all cart items of a single user
def getAllCartItems(user_id):
    cart_items = []
    for item in collection.find({'userId': user_id}):
        cart_items.append(item)
    
    return cart_items

@app.route('/delete_from_cart/<user_id>', methods = ['DELETE'])
def delete_from_cart(user_id):
    if getAllCartItems(user_id).length() > 0:
        collection.delete_many({'userId': user_id})
        return jsonify({'success': True}), 200
    else:
        return jsonify({'success': False, 'message': 'Cart is empty'})

#  port 5002
if __name__ == '__main__':
    app.run(port = 5003, debug = True)