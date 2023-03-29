from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

# enable CORS
CORS(app)

# Connect to MongoDB
client = MongoClient(
    'mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['listingsMS']
collection = db['listings1']

# Help functions -- Start


def get_quantity_by_product_id(product_id):
    product = collection.find_one({'productID': product_id})
    if product:
        return product['quantity']
    else:
        return None
# Help functions -- End

# Get All Products from listing
@app.route('/products', methods=['GET'])
def getAllProducts():
    try:
        products = list(collection.find())
        product_list = []
        for product in products:
            product_dict = {
                'code': 200,
                'productID': product["productID"],
                'itemName': product['itemName'],
                'quantity': product['quantity'],
                'price': product['price'],
                'dateOfPost': product['dateOfPost'],
                'availability': product['availability'],
                # 'location': product['location'],
                'imgURL': product["imgURL"]
            }
            product_list.append(product_dict)
        return jsonify(product_list)
    except Exception as e:
        return jsonify({'code': 404, 'error': str(e)}), 404

# Get 1 Product
@app.route('/products/<int:productID>', methods=['GET'])
def getProductByID(productID):
    product = collection.find_one({'productID': productID})
    if product:
        product_dict = {
            'productID': product["productID"],
            'itemName': product['itemName'],
            'quantity': product['quantity'],
            'price': product['price'],
            'dateOfPost': product['dateOfPost'],
            'availability': product['availability'],
            # 'location': product['location'],
            'imgURL': product["imgURL"]
        }
        return jsonify(product_dict)
    else:
        return jsonify(
            {
                'code': 404,
                'error': 'Product not found'
            }
        ), 404


@app.route('/products/<int:productID>/quantity', methods=['GET'])
def get_product_quantity(productID):
    quantity = get_quantity_by_product_id(productID)
    if quantity is not None:
        return jsonify(
            {
                'code': 200,
                'productID': productID,
                'quantity': quantity
            }
        ), 200
    else:
        return jsonify(
            {
                'code': 404,
                'error': 'Product not found'
            }
        ), 404

# Add product to db
@app.route('/add_product', methods=['POST'])
def add_product():
    productID = get_next_sequence_value("productid")

    data = request.get_json()
    itemName = data["itemName"]
    quantity = data['quantity']
    price = data['price']
    dateOfPost = data['dateOfPost']
    availability = data['availability']
    # location = data['location']
    imgURL = data["imgURL"]

    # ADD ERROR HANDLING

    collection.insert_one
    (
        {
            'productID': productID,
            'itemName': itemName,
            'quantity': quantity,
            'price': price,
            'dateOfPost': dateOfPost,
            'availability': availability,
            # 'location': location,
            "imgURL": imgURL
        }
    )
    return getAllProducts()


def get_next_sequence_value(sequence_name):
    counter = db.counters
    sequence_value = counter.find_one_and_update(
        {"_id": sequence_name}, {"$inc": {"seq": 1}})
    return sequence_value['seq']


@app.route('/edit/<product_id>', methods=['PUT'])
def edit_product(product_id, soldQuantity):
    product = collection.find({_id: product_id})
    data = request.get_json()
    itemName = data["itemName"]
    price = data['price']
    dateOfPost = data['dateOfPost']
    availability = data['availability']
    imgURL = data["imgURL"]
    # location = data['location']
    quantity = data['quantity'] - soldQuantity

    collection.update_one
    (
        {
            'productID': product_id,
            'itemName': itemName,
            'quantity': quantity,
            'price': price,
            'dateOfPost': dateOfPost,
            'availability': availability,
            # "location": location,
            "imgURL": imgURL
        }
    )
    return getAllProducts()

# removing sold OR no quantity products


@app.route('/delete/<product_id>', methods=['DELETE'])
def delete_product(product_id):
    collection.delete_one({_id: product_id})
    return getAllProducts()


if __name__ == '__main__':
    app.run(port=5001, debug=True)
