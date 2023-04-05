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
                'address': product['address'],
                'imgURL': product["imgURL"]
            }
            product_list.append(product_dict)
        return jsonify(
            {
                "code": 200,
                "message": "Retrieved all products",
                "data": {
                    "products": product_list
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
            'address': product['address'],
            'imgURL': product["imgURL"]
        }
        return jsonify(
            {
                "code": 200,
                "message": "Retrieved 1 product",
                "data": {
                    "product": product_dict
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

# # FOR PAYMENT
# @app.route('/check_item_quantity', methods=['POST'])
# def check_item_quantity():
#     shoppingCart = request.get_json()
#     for eachItem in shoppingCart:
#         product_ID = eachItem['productID']
#         productName = eachItem['itemName']

#         product = collection.find_one({'productID': product_ID})
#         product_dict = {
#             'sellerID': product['sellerID'],
#             'productID': product["productID"],
#             'itemName': product['itemName'],
#             'quantity': product['quantity'],
#             'price': product['price'],
#             'dateOfPost': product['dateOfPost'],
#             'address': product['address'],
#             'imgURL': product["imgURL"]
#         }

#         checkQuantity = product_dict['quantity']
#         currentQuantity = eachItem['inputQuantity']

#         if currentQuantity > checkQuantity:
#             return jsonify({
#                 'code': 400,
#                 'error': f"Checkout error: {productName} is currently unavailable due to not enough inventory quantity"
#             }), 400


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
            'address': address,
            "imgURL": imgURL})
        return jsonify(
            {
                "code": 200,
                "message": "Successfully added product",
                "data": {
                    "all_products": getAllProducts()
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


@app.route('/update_sold_product_qty', methods=['PUT'])
def edit_product():
    try:
        data = request.get_json()
        productID = data["productID"]
        soldQuantity = data['soldQuantity']

        collection.update_one({"productID": productID}, {
                              "$inc": {"quantity": -soldQuantity}})
        print("updated")
        return jsonify({
                "code": 200,
                "message": "Updated product quantity",
                "data": {
                    "product": getProductByID_helper_function(productID)
                }
            }), 200

    except:
        return jsonify(
            {
                "code": 400,
                "message": "Error updating product quantity",
            }
        ), 400
    


# get product by id helper function
def getProductByID_helper_function(productID):
    product = collection.find_one({'productID': productID})
    if product:
        product_dict = {
            'sellerID': product['sellerID'],
            'productID': product["productID"],
            'itemName': product['itemName'],
            'quantity': product['quantity'],
            'price': product['price'],
            'dateOfPost': product['dateOfPost'],
            'address': product['address'],
            'imgURL': product["imgURL"]
        }
        return product_dict
    


# removing sold OR no quantity products
@app.route('/remove_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:

        collection.delete_many({"productID": product_id})

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
