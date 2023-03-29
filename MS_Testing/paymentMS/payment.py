import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Replace with your own Stripe API keys
stripe.api_key = 'sk_test_51MltK7EBOpB8WMsEGsB51xLyAgs77LcOmFOr8mmzF2cPB0Fb0TeKXRRcv24nI6GId4wSEWovYyvWfx8iL2SmKpP800dNlhECw0'


@app.route('/create_payment_intent', methods=['POST'])
def create_payment_intent():
    if request.is_json:
        data = request.json
        print(data)
        total_amount = 0
        checkout_description = ", ".join(
            [f"{item['itemName']} x{item['quantity']}" for item in data])
        for eachItem in data:
            item_quantity = eachItem['quantity']
        # if product_id not in PRODUCTS:
        #     return jsonify({'error': 'Invalid product ID'}), 400

        # product = PRODUCTS[product_id]

        # Calculate the total amount
            # Stripe expects the amount in cents
            amount = int(eachItem['price']) * item_quantity * 100
            total_amount += amount

        try:
            # Create a new PaymentIntent
            payment_intent = stripe.PaymentIntent.create(
                amount=total_amount,
                currency='usd',
                description=checkout_description,
            )
            return jsonify({
                'code': 200,
                'clientSecret': payment_intent['client_secret'],
                'description': payment_intent['description']
            })

        except Exception as e:
            print("Error:", e)
            print(traceback.format_exc())
            return jsonify(
                {
                    'code': 400, 
                    'error': str(e)
                }
            ), 400

    else:
        return jsonify(
            {
            'code': 400, 
            'error': 'Invalid JSON request'
            }
            ), 400


if __name__ == '__main__':
    app.run(port=5002, debug=True)
