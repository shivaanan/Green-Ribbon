from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)

# enable CORS
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['listingsMS']
collection = db['listings1']



@app.route('/products', methods = ['GET'])
def getAllProducts():
	products = list(collection.find())
	product_list = []
	for product in products:
		product_dict = {'productID' : product["productID"], 'itemName': product['itemName'], 'quantity': product['quantity'], 'price': product['price'], 'dateOfPost': product['dateOfPost'], 'availability': product['availability'], 'imgURL' : product["imgURL"]}
		product_list.append(product_dict)
	return product_list


@app.route('/add_product', methods=['POST'])
def add_product():
	productID = get_next_sequence_value("productid")
	# -----------------------------------------------------------------------------
	# testing using postman body
	data = request.get_json()
	itemName = data["itemName"]
	quantity = data['quantity']
	price = data['price']
	dateOfPost = data['dateOfPost']
	availability = data['availability']
	imgURL = data["imgURL"]
	# -----------------------------------------------------------------------------

	# itemName = request.form["itemName"]
	# quantity = request.form['quantity']
	# price = request.form['price']
	# dateOfPurchase = request.form['datOfPurchase']
	# availability = request.form['availability']

	# ADD ERROR HANDLING

	collection.insert_one({'productID' : productID,'itemName': itemName, 'quantity': quantity, 'price': price, 'dateOfPost': dateOfPost, 'availability': availability, "imgURL" : imgURL})
	return getAllProducts()

def get_next_sequence_value(sequence_name):
	counter = db.counters
	sequence_value = counter.find_one_and_update({"_id": sequence_name}, {"$inc": {"seq": 1}})
	return sequence_value['seq']

## editing the item quantity in the 
@app.route('/edit/<product_id>', methods=['PUT'])
def edit_product(product_id, soldQuantity):
	product = collection.find({_id: product_id})
	data = request.get_json()
	itemName = data["itemName"]
	price = data['price']
	dateOfPost = data['dateOfPost']
	availability = data['availability']
	imgURL = data["imgURL"]
	quantity = data['quantity'] - soldQuantity


	collection.update_one({'productID' : product_id,'itemName': itemName, 'quantity': quantity, 'price': price, 'dateOfPost': dateOfPost, 'availability': availability, "imgURL" : imgURL})
	return getAllProducts()

## removing sold OR no quantity products
@app.route('/delete/<product_id>', methods = ['DELETE'])
def delete_product(product_id):
	collection.delete_one({_id: product_id})
	return getAllProducts()

if __name__ == '__main__':
      app.run(debug=True)