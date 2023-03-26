document.addEventListener("DOMContentLoaded", () => {
  const publicKey =
    "pk_test_51MltK7EBOpB8WMsEafwEYrSYcLFCnAasAwZceaxQYgfYrZCxiqFymPFqCAhtz4BL0L7XB1HwKWzK53blzlcakXAj00b5LtAwQQ"; // Replace with your Stripe public key

  const stripe = Stripe(publicKey);
  const elements = stripe.elements();
  const card = elements.create("card");
  card.mount("#card-element");

  const paymentForm = document.getElementById("payment-form");
  paymentForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const response = await fetch(
      "http://127.0.0.1:8000/create_payment_intent",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          productID: 0,
          quantity: 2, // or get this value from a form input
        }),
      }
    );

    if (!response.ok) {
      const errorData = await response.json();
      console.error("Backend error:", errorData.error);
      return;
    }

    const data = await response.json();
    // Card Holder Name
    const cardHolderName = document.getElementById('cardHolderName').value
    const result = await stripe.confirmCardPayment(data.clientSecret, {
      payment_method: {
        card: card,
        billing_details: {
          name: cardHolderName, // Replace with a form input for the user's name
        },
      },
    });

    if (result.error) {
      console.error("Payment failed:", result.error.message);
    } else {
      console.log("Payment succeeded:", result.paymentIntent.id);
      window.location.href = "thanks.html"; // Redirect to thanks.html after successful payment
    }

    const errorMessageElement = document.getElementById("error-message");

    // ...
    if (result.error) {
      console.error("Payment failed:", result.error.message);
      errorMessageElement.textContent = result.error.message;
      errorMessageElement.style.display = "block";
    } else {
      console.log("Payment succeeded:", result.paymentIntent.id);
      errorMessageElement.style.display = "none";
      window.location.href = "thanks.html"; // Redirect to thanks.html after successful payment
    }
  });
});
