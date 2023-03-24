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

@app.route('/add_to_cart',methods = ['POST'])
def add_to_cart(productID):
    product = getProductByID(productID)
    data = request.get_json()
    itemName = data["itemName"]
    quantity = data['quantity']
    price = data['price']
    dateOfPost = data['dateOfPost']
    availability = data['availability']
    # location = data['location']
    imgURL = data["imgURL"]
    if product is not null and itemName not in cart:
        cart[itemName] = [quantity, price, dateOfPost, availability, '''location''', imgURL]

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

    return cart

#  port 5002
if __name__ == '__main__':
    app.run(port = 5002, debug = True)