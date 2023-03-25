// OLD PAYMENT SYSTEM - START
// Need to add productID into the parameter
// async function checkOut() {
//     // console.log(productID);
    
//     try {
//         const frontendBaseUrl = window.location.origin;

//         const response = await axios.post(
//             "http://127.0.0.1:5100/buy_item",
//             {
//                 product_id: 0,
//                 // frontend_base_url: frontendBaseUrl
//             }
//         );

//         const data = response.data.data.payment_result.data;
//         // console.log(data)
        
//         if (data.checkout_session_id) {
//             const stripe = Stripe(data.checkout_public_key);
//             stripe.redirectToCheckout({ sessionId: data.checkout_session_id });
//         } else {
//             // Handle errors (e.g., Price not found for the given product)
//             console.error("Error:", data.error);
//         }
//     } catch (error) {
//         console.error("Error:", error);
//     }
// }
// OLD PAYMENT SYSTEM - END