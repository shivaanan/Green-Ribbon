from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import _get_object_size

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['listingsMS']
collection = db['listings1']

@app.route('/products', methods = ['GET'])
def index():
	products = list(collection.find())
	product_list = []
	for product in products:
		product_dict = {'itemName': product['itemName'], 'quantity': product['quantity'], 'price': product['price'], 'dateOfPurchase': product['dateOfPurchase'], 'availability': product['availability']}
		product_list.append(product_dict)
	return jsonify(product_list)


@app.route('/add_product', methods=['POST'])
def add_product():
      itemName = request.form['itemName']
      quantity = request.form['quantity']
      price = request.form['price']
      dateOfPurchase = request.form['datOfPurchase']
      availability = request.form['availability']

      collection.insert_one({'itemName': itemName, 'quantity': quantity, 'price': price, 'dateOfPurchase': dateOfPurchase, 'availability': availability})
      return jsonify(collection)

@app.route('/edit/<product_id>', methods=['POST'])
def edit_product(product_id):
      product = collection.find_one({'_id': ObjectId(product_id)})
      itemName = request.form['itemName']
      quantity = request.form['quantity']
      price = request.form['price']
      dateOfPurchase = request.form['datOfPurchase']
      availability = request.form['availability']
      collection.update_one({'_id': ObjectId(product_id)}, {'$set': {'itemName': itemName, 'quantity': quantity, 'price': price, 'dateOfPurchase': dateOfPurchase, 'availability': availability}})
      return jsonify(collection)

@app.route('/delete/<product_id>')
def delete_product(product_id):
      collection.delete_one({'_id': ObjectId(product_id)})
      return jsonify(collection)

if __name__ == '__main__':
      app.run(debug=True)