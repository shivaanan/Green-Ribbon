from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime

import stripe
import requests


app = Flask(__name__)
CORS(app)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_51MltK7EBOpB8WMsEafwEYrSYcLFCnAasAwZceaxQYgfYrZCxiqFymPFqCAhtz4BL0L7XB1HwKWzK53blzlcakXAj00b5LtAwQQ'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51MltK7EBOpB8WMsEGsB51xLyAgs77LcOmFOr8mmzF2cPB0Fb0TeKXRRcv24nI6GId4wSEWovYyvWfx8iL2SmKpP800dNlhECw0'

stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    product = request.json

    try:

        # Convert price to cents
        product_price = int(float(product['price']) * 100)

        # Create a new Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',  # Change this to your desired currency
                    'product_data': {
                        'name': product['itemName'],
                    },
                    'unit_amount': product_price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.url_root + 'thanks',
            cancel_url=request.url_root + 'home',
        )
        
        dateOfPurchase = datetime.now()
        return jsonify({
            "code": 201,
            "data": {
                'dateOfPurchase': dateOfPurchase,
                'itemPurchase': product,
                'checkout_session_id': checkout_session.id,
                'checkout_public_key': app.config['STRIPE_PUBLIC_KEY'],
            }
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/thanks')
def thanks():
    return send_from_directory('../../Frontend', 'thanks.html')


@app.route('/home')
def home():
    return send_from_directory('../../Frontend', 'home.html')


if __name__ == '__main__':
    app.run(port=5002, debug=True)
