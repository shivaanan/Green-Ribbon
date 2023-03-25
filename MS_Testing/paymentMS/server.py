import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your own Stripe API keys
stripe.api_key = 'sk_test_51MltK7EBOpB8WMsEGsB51xLyAgs77LcOmFOr8mmzF2cPB0Fb0TeKXRRcv24nI6GId4wSEWovYyvWfx8iL2SmKpP800dNlhECw0'


PRODUCTS = {
    0: {
        'itemName': 'Chair',
        'price': '2',
        'productID': 0,
        'quantity': 8
    }
}

@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    data = request.get_json()
    product_id = data.get('productID')
    quantity = data.get('quantity', 1)

    if product_id not in PRODUCTS:
        return jsonify({'error': 'Invalid product ID'}), 400

    product = PRODUCTS[product_id]

    # Calculate the total amount
    amount = int(product['price']) * quantity * 100  # Stripe expects the amount in cents

    try:
        # Create a new PaymentIntent
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            description=f"{product['itemName']} x{quantity}",
        )
        return jsonify({
            'clientSecret': payment_intent['client_secret'],
            'description': payment_intent['description']
        })

    except Exception as e:
        print("Error:", e)
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(port=8000)
