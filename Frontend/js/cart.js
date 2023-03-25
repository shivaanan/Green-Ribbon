// Need to add productID into the parameter
async function checkOut() {
    // console.log(productID);

    try {
        const response = await axios.post(
            "http://127.0.0.1:5002/create-checkout-session",
            {
                product_id: 0,
            }
        );

        const data = response.data;

        if (data.checkout_session_id) {
            const stripe = Stripe(data.checkout_public_key);
            stripe.redirectToCheckout({ sessionId: data.checkout_session_id });
        } else {
            // Handle errors (e.g., Price not found for the given product)
            console.error("Error:", data.error);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}