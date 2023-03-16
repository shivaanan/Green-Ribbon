import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/add_to_cart',methods = ['POST'])

def add_to_cart():
    return json.dumps({'success': True})

if __name__ == '__main__':
    app.run()