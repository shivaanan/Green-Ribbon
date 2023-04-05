import stripe
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Replace with your own Stripe API keys
stripe.api_key = 'sk_test_51MltK7EBOpB8WMsEGsB51xLyAgs77LcOmFOr8mmzF2cPB0Fb0TeKXRRcv24nI6GId4wSEWovYyvWfx8iL2SmKpP800dNlhECw0'


@app.route('/payment', methods=['POST'])
def payment():
    data = request.json
    print("TEST data (START)")
    print(data)
    print("TEST data (END)")
    shoppingCart = data['dataObj']
    card_details = data['cardDetails']
    cardHolderName = data['cardName']
    # print("print card (START)")
    # print(card_details)
    # print("print card (END)")
    # print("TEST shoppingCart (start)")
    # print(shoppingCart)
    # print("TEST shoppingCart (end)")
    # print("TEST cardName (start)")
    # print(cardHolderName)
    # print("TEST cardName (end)")
    total_amount = 0
    # ======== CHECKOUT DESCRIPTION (START) ========
    checkout_description = ", ".join(
        [f"{item['itemName']} x{item['inputQuantity']}" for item in shoppingCart])
    # ======== CHECKOUT DESCRIPTION (END) ========

    # print("TEST card_details (START)")
    # print(card_details)
    # print("TEST card_details (END)")

    for eachItem in shoppingCart:
        item_quantity = eachItem['inputQuantity']
    # if product_id not in PRODUCTS:
    #     return jsonify({'error': 'Invalid product ID'}), 400

    # product = PRODUCTS[product_id]

    # Calculate the total amount
        # Stripe expects the amount in cents
        amount = int(eachItem['price'] * item_quantity * 100 * 1.08)
        total_amount += amount

    checkout_amount = total_amount/100 # in dollars
    purchase_summary = {
         "checkoutDescription":checkout_description,
         "totalAmount": checkout_amount
    }
    # print(f"TOTAL AMOUNT: {total_amount}")
    # print(f"purchase summary: {purchase_summary}")
    try:
        # stringShoppingCart = json.dumps(shoppingCart)
        # Create a new PaymentIntent
        print("IM HERE!")
        print(total_amount)
        print(type(total_amount))
        print(checkout_description)
        print(type(checkout_description))

        payment_intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency='usd',
            # description=f"{shoppingCart}",
            # description=stringShoppingCart,
            description=checkout_description,
        )
        print("TEST paymentIntent (START)")
        print(payment_intent)
        print("TEST paymentIntent (END)")

        # card_details = {
        #     "number": "4242 4242 4242 4242",
        #     "exp_month": "04",
        #     "exp_year": "24",
        #     "cvc": "242"
        # }
        
        token_response = stripe.Token.create(card=card_details)
        
        paymentResult = stripe.PaymentIntent.confirm(
                payment_intent['id'],
                payment_method_data={
                    "type": "card",
                    "card": {
                        "token": token_response,
                    },
                    "billing_details": {
                        "name": cardHolderName,  # Replace with a form input for the user's name
                    },
                },
            )
        # print("TEST result (START)")
        # print(paymentResult)
        # print("TEST result (END)")
        return jsonify({
            'code': 201,
            'paymentStatus':'Payment_Successful',
            'message':'Payment Successful! Thank you for shopping with us :)',
            'description': shoppingCart,
            'purchaseSummary':purchase_summary,
        }), 201
        

    except:
            return jsonify({
            "code": 400,
            'paymentStatus':'Payment_Unsuccessful',
            "message": "Payment Unsuccessful!",
        }), 400
    

@app.route('/refund', methods=['POST'])
def refund():
    data = request.json
    print("TEST data (START)")
    print(data)
    print("TEST data (END)")
    shoppingCart = data['dataObj']
    card_details = data['cardDetails']
    cardHolderName = data['cardName']
    print("print card (START)")
    print(card_details)
    print("print card (END)")
    
    print("TEST cardName (start)")
    print(cardHolderName)
    print("TEST cardName (end)")

    shoppingCart = [shoppingCart]
    print("TEST shoppingCart (start)")
    print(shoppingCart)
    print("TEST shoppingCart (end)")
    
    total_amount = 0
    # ======== CHECKOUT DESCRIPTION (START) ========
    checkout_description = ", ".join(
        [f"{item['itemName']} x{item['quantity']}" for item in shoppingCart])
    # ======== CHECKOUT DESCRIPTION (END) ========

    # print("TEST card_details (START)")
    # print(card_details)
    # print("TEST card_details (END)")
    
    for eachItem in shoppingCart:
        item_quantity = eachItem['quantity']
    # if product_id not in PRODUCTS:
    #     return jsonify({'error': 'Invalid product ID'}), 400

    # product = PRODUCTS[product_id]

    # Calculate the total amount
        # Stripe expects the amount in cents
        amount = int(eachItem['price'] * item_quantity * 100 * 1.08)
        total_amount += amount

    checkout_amount = total_amount/100 # in dollars
    purchase_summary = {
         "checkoutDescription":checkout_description,
         "totalAmount": checkout_amount
    }
    # print(f"TOTAL AMOUNT: {total_amount}")
    # print(f"purchase summary: {purchase_summary}")
    try:
        # stringShoppingCart = json.dumps(shoppingCart)
        # Create a new PaymentIntent
        print("IM HERE!")
        print(total_amount)
        print(type(total_amount))
        print(checkout_description)
        print(type(checkout_description))

        payment_intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency='usd',
            # description=f"{shoppingCart}",
            # description=stringShoppingCart,
            description=checkout_description,
        )
        print("TEST paymentIntent (START)")
        print(payment_intent)
        print("TEST paymentIntent (END)")

        # card_details = {
        #     "number": "4242 4242 4242 4242",
        #     "exp_month": "04",
        #     "exp_year": "24",
        #     "cvc": "242"
        # }
        
        token_response = stripe.Token.create(card=card_details)
        
        paymentResult = stripe.PaymentIntent.confirm(
                payment_intent['id'],
                payment_method_data={
                    "type": "card",
                    "card": {
                        "token": token_response,
                    },
                    "billing_details": {
                        "name": cardHolderName,  # Replace with a form input for the user's name
                    },
                },
            )
        # print("TEST result (START)")
        # print(paymentResult)
        # print("TEST result (END)")
        return jsonify({
            'code': 201,
            'paymentStatus':'Payment_Successful',
            'message':'Payment Successful! Thank you for shopping with us :)',
            'description': shoppingCart,
            'purchaseSummary':purchase_summary,
        }), 201
        

    except:
            return jsonify({
            "code": 400,
            'paymentStatus':'Payment_Unsuccessful',
            "message": "Payment Unsuccessful!",
        }), 400
        


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
