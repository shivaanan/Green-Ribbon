from flask import Flask, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

# enable CORS
CORS(app)

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient(
    'mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['CartDB']
collection = db['addToCart']

# Get All Products
@app.route('/products', methods=['GET'])
def getAllProducts():
    try:
        products = list(collection.find())
        product_list = []
        for product in products:
            product_dict = {'code':200,'productID': product["productID"], 'itemName': product['itemName'], 'quantity': product['quantity'],
                            'price': product['price'], 'dateOfPost': product['dateOfPost'], 'availability': product['availability'], 'imgURL': product["imgURL"]}
            product_list.append(product_dict)
        return jsonify(product_list)
    except Exception as e:
        return jsonify({'code':404,'error': str(e)}),404

def get_next_sequence_value(sequence_name):
    counter = db.counters
    sequence_value = counter.find_one_and_update(
        {"_id": sequence_name}, {"$inc": {"seq": 1}})
    return sequence_value['seq']

@app.route('/add_to_cart',methods = ['POST'])
def add_to_cart():
    productID = get_next_sequence_value("productid")
    data = request.get_json()
    itemName = data["itemName"]
    quantity = data['quantity']
    price = data['price']
    dateOfPost = data['dateOfPost']
    availability = data['availability']
    imgURL = data["imgURL"]
    
    collection.insert_one({
        'productID': productID, 
        'itemName': itemName, 
        'quantity': quantity,
        'price': price, 
        'dateOfPost': dateOfPost, 
        'availability': availability, 
        'imgURL': imgURL
    })

    return 

if __name__ == '__main__':
    app.run(port = 5002, debug = True)