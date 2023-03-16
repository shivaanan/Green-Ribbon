from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)

# Set up the MongoDB client and database
client = MongoClient('mongodb+srv://esdg6t4:zJZcldRJaXWpX77z@listingsmicroservice.rkrskux.mongodb.net/?retryWrites=true&w=majority')
db = client['listingsMS']
collection = db['listings1']

# Define a route that adds a document to MongoDB
@app.route('/add_data')
def add_data():
      # Define the document to be added
      document = {
            "item": "chair",
            "qty": 25,
            "date": "13-03-2023",
            "availability": True
      }
      
      # Add the document to the collection
      collection.insert_one(document)
      
      # Return a message indicating success
      return "Data added successfully"

if __name__ == '__main__':
      app.run(debug=True)

@app.route('/test')
def test():      
      # Return a message indicating success
      return "testing..."

if __name__ == '__main__':
      app.run(debug=True)

###############################################################################################################
## accessing pre-populated data
# Find all documents in the collection
documents = collection.find()

# Iterate over the documents and print them
for document in documents:
      print(document)