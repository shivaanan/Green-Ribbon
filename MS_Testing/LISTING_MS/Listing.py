from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS
from os import environ

app = Flask(__name__)

# enable CORS
CORS(app)

# Connect to MongoDB
client = MongoClient(
    'mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['listingsMS']
collection = db['listings1']

# Get All Products from listing
@app.route('/products', methods=['GET'])
def getAllProducts():
    try:
        
        products = list(collection.find())
        print(products)
        print("testing")
        product_list = []

        for product in products:
            product_dict = {
                'sellerID': product['sellerID'],
                'productID': product["productID"],
                'itemName': product['itemName'],
                'quantity': product['quantity'],
                'price': product['price'],
                'dateOfPost': product['dateOfPost'],
                'availability': product['availability'],
                'address': product['address'],
                'imgURL': product["imgURL"]
            }
            product_list.append(product_dict)
        return jsonify(
            {
                "code": 200, 
                "message": "Retrieved all products",
                "data" : {
                    "products" : product_list
                }
            }
        ), 200
    
    except:
        return jsonify( 
            {
                "code": 400, 
                "message": "Unable to retrieve all products"
            }
        ), 400 

# Get 1 Product
@app.route('/products/<int:productID>', methods=['GET'])
def getProductByID(productID):
    product = collection.find_one({'productID': productID})
    if product:
        product_dict = {
            'sellerID': product['sellerID'],
            'productID': product["productID"],
            'itemName': product['itemName'],
            'quantity': product['quantity'],
            'price': product['price'],
            'dateOfPost': product['dateOfPost'],
            'availability': product['availability'],
            'address': product['address'],
            'imgURL': product["imgURL"]
        }
        return jsonify(
            {
                "code": 200, 
                "message": "Retrieved 1 product",
                "data" : {
                    "products" : product_dict
                }
            }
        ), 200
    else:
        return jsonify( 
            {
                "code": 400, 
                "message": "Product not found"
            }
        ), 400 

# ========================== EXTRA ==========================
# @app.route('/products/<int:productID>/quantity', methods=['GET'])
# def get_product_quantity(productID):
#     quantity = get_quantity_by_product_id(productID)
#     if quantity is not None:
#         return jsonify(
#             {
#                 'code': 200,
#                 'productID': productID,
#                 'quantity': quantity
#             }
#         ), 200
#     else:
#         return jsonify(
#             {
#                 'code': 404,
#                 'error': 'Product not found'
#             }
#         ), 404
# Helper function for the route "/products/<int:productID>/quantity" -- Start
# def get_quantity_by_product_id(product_id):
#     product = collection.find_one({'productID': product_id})
#     if product:
#         return product['quantity']
#     else:
#         return None
# Helper function for the route "/products/<int:productID>/quantity" -- End
# ========================== EXTRA ==========================


# Not in scenario
# Add product to db
@app.route('/add_product', methods=['POST'])
def add_product():
    try:
        productID = get_next_sequence_value("productid")

        data = request.get_json()
        sellerID = data["sellerID"]
        itemName = data["itemName"]
        quantity = data['quantity']
        price = data['price']
        dateOfPost = data['dateOfPost']
        availability = data['availability']
        address = data['address']
        imgURL = data["imgURL"]

        # ADD ERROR HANDLING

        collection.insert_one({
                'productID': productID,
                'sellerID': sellerID,
                'itemName': itemName,
                'quantity': quantity,
                'price': price,
                'dateOfPost': dateOfPost,
                'availability': availability,
                'address': address,
                "imgURL": imgURL})
        return jsonify(
            {
                "code": 200, 
                "message": "Successfully added product",
                "data" : {
                    "all_products" : getAllProducts()
                }   
            }
        ), 200
    
    except:
        return jsonify(
            {
                "code": 400, 
                "message": "Error updating product quantity",
            }
        ), 400


def get_next_sequence_value(sequence_name):
    counter = db.counters
    sequence_value = counter.find_one_and_update(
        {"_id": sequence_name}, {"$inc": {"seq": 1}})
    return sequence_value['seq']


@app.route('/update_product_qty', methods=['PUT'])
def edit_product():
    try:
        data = request.get_json()
        productID = data["productID"]
        soldQuantity = data['soldQuantity']

        collection.update_one({"productID": productID}, {"$inc": {"quantity": -soldQuantity}})

        return jsonify(
            {
                "code": 200, 
                "message": "Updated product quantity",
            }
        ), 200
    
    except:
        return jsonify(
            {
                "code": 400, 
                "message": "Error updating product quantity",
            }
        ), 400

# removing sold OR no quantity products


@app.route('/remove_product/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    try: 

        collection.delete_one({_id: product_id})

        return jsonify(
            {
                "code": 200, 
                "message": "Product Successfully Deleted",
            }
        ), 200
    
    except:
        return jsonify(
            {
                "code": 400, 
                "message": "Error deleting product",
            }
        ), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
