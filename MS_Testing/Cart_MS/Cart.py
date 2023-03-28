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

# Get All Cart Items
@app.route('/allCartItems', methods=['GET'])
def getAllProducts():
    try:
        cart_items = list(collection.find())
        cart_list = []
        for a_item in cart_items:
            cart_dict = {
                'productID': a_item["productID"], 
                'itemName': a_item['itemName'], 
                'quantity': a_item['quantity'],
                'price': a_item['price'], 
                'dateOfPost': a_item['dateOfPost'], 
                'availability': a_item['availability'],
                # 'location': a_item['location'],
                'imgURL': a_item["imgURL"]
            }
            cart_list.append(cart_dict)
        return jsonify(cart_list)
    
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

#  port 5002
if __name__ == '__main__':
    app.run(port = 5003, debug = True)