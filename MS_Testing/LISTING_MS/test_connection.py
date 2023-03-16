from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['listingsMS']
collection = db['listings1']


@app.route('/data', methods=['GET'])
def get_data():
      """
      Endpoint to get data from the MongoDB collection.
      Returns a JSON object with the data.
      """
      data = []
      for document in collection.find():
            document['_id'] = str(document['_id'])
            data.append(document)
      return jsonify(data)

if __name__ == '__main__':
      app.run()