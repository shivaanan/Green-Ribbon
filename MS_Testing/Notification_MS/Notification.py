#!/usr/bin/env python3

import os
import json
from flask import Flask, request
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = "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"
app = Flask(__name__)

@app.route('/paymentNotification', methods=['POST'])
def paymentNotification():
    data = request.json
    # code = data.get('code', 0)
    # message = data.get('message', '')

    # # Extract email address from data (assuming it's included)
    # email = data.get('email', '')

    print("Test data (START)")
    print(data)
    print("Test data (END)")

    # code = data['code']
    paymentStatus = data['paymentStatus']
    email="lintao199@gmail.com"

    if paymentStatus == 'Payment_Successful':
        subject = "Purchase Successful"
        message = f"You have purchased {data['purchaseSummary']['checkoutDescription']}. Total amount is ${data['purchaseSummary']['totalAmount']}USD"
    elif paymentStatus == 'Payment_Unsuccessful':
        subject = "Purchase Unsuccessful"
        message = "Purchase Unsuccessful! Invalid card details!"
    else:
        return {"error": "Invalid status code"}, 400

    # Send email using SendGrid
    send_email(email, subject, message)

    return {"message": "Email sent"}

def send_email(to_email, subject, content):
    message = Mail(
        from_email="esdg6t4@gmail.com",
        to_emails=to_email,
        subject=subject,
        plain_text_content=content
    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        # print("TEST (START)")
        # print(sg)
        # print("BREAK")
        # print(response)
        # print("TEST (END)")

        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
        print("Error sending email")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
