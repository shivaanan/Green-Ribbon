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

    const getCartResponse = await fetch('http://127.0.0.1:5100/get_cart/' + userId,{
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
    console.log("FUCK")
    console.log(getCartResponse)

    const paymentResponse = await fetch("http://127.0.0.1:5100/buy_item", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(
        [
          {
            availability: true,
            dateOfPost: "02-03-2023",
            imgURL:
              "https://images.unsplash.com/photo-1581539250439-c96689b516dd?ixlib=rb-…",
            itemName: "Chair",
            price: "2",
            productID: 0,
            quantity: 8,
          },
          {
            availability: true,
            dateOfPost: "02-03-2023",
            imgURL:
              "https://images.unsplash.com/photo-1533090481720-856c6e3c1fdc?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=388&q=80",
            itemName: "Table",
            price: "100",
            productID: 1,
            quantity: 1,
          },
        ]
        // productID: [0,1],
        // quantity: 2, // or get this value from a form input
      ),
    });

    if (!paymentResponse.ok) {
      const errorData = await paymentResponse.json();
      console.error("Backend error:", errorData.error);
      return;
    }

    const data = await paymentResponse.json();
    // console.log(data)
    // console.log(data.clientSecret)
    
    // Card Holder Name
    const cardHolderName = document.getElementById("cardHolderName").value;
    const result = await stripe.confirmCardPayment(data.data.payment_result.clientSecret, {
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
