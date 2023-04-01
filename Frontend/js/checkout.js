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
    var userId = sessionStorage.getItem("userId");
    // console.log("WHEN CLICK CHECKOUT -- START");
    // console.log(userId);
    const getCartResponse = await fetch(
      "http://127.0.0.1:5100/get_cart/" + userId,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    const jsonData = await getCartResponse.json();
    // console.log(jsonData)

    const paymentResponse = await fetch("http://127.0.0.1:5100/buy_item", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(
        jsonData
        // ======================== Sample Dataset of jsonData (START) ========================
        // [
        //   {
        //     "dateOfPost": "02-03-2023",
        //     "imgURL": "https://images.unsplash.com/photo-1581539250439-c96689b516dd?ixlib=rb-…",
        //     "inputQuantity": 1,
        //     "itemName": "Chair",
        //     "price": "2",
        //     "productID": 0,
        //     "userId": "fVHw0ezNLlUbxhJYmpCxi8FklLp1",
        //     "_id": "6425569b10754c27d62fe433"
        //   },
        //   {
        //    "dateOfPost": "21-03-2023",
        //    "imgURL": "https://images.unsplash.com/photo-1554757387-fa0367573d09?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8bm90ZWJvb2t8ZW58MHx8MHx8&auto=format&fit=crop&w=800&q=60",
        //    "inputQuantity": 3,
        //    "itemName": "Notebook",
        //    "price": "5",
        //    "productID": 3,
        //    "userId": "fVHw0ezNLlUbxhJYmpCxi8FklLp1",
        //    "_id": "642556d110754c27d62fe435"
        //   },
        // ]
        // ======================== Sample Dataset of jsonData (END) ========================
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
    const result = await stripe.confirmCardPayment(
      data.data.payment_result.clientSecret,
      {
        payment_method: {
          card: card,
          billing_details: {
            name: cardHolderName, // Replace with a form input for the user's name
          },
        },
      }
    );
      
    if (result.error) {
      // PAYMENT FAILED
      console.error("Payment failed:", result.error.message);
    } else {
      // PAYMENT SUCCESS
      console.log("Payment succeeded:", result.paymentIntent.id);
      
      purchasedItems_string = result.paymentIntent.description
      // console.log("TEST purchaseItems_string START")
      // console.log(purchasedItems_string)
      // console.log("TEST purchaseItems_string END")

      purchasedItems_string = purchasedItems_string.replace(/'/g, "\"");
      purchasedItems_object = JSON.parse(purchasedItems_string);
      // console.log("TEST purchaseItems_object START")
      // console.log(purchasedItems_object)
      // console.log("TEST purchaseItems_object END")
      
      // ========= ORDER HISTORY (START) =========
      // const paymentHistoryResponse = await fetch(
      //   "http://127.0.0.1:5100/" + userId,
      //   {
      //     method: "POST",
      //     headers: {
      //       "Content-Type": "application/json",
      //     },
      //     body: JSON.stringify(
      //       purchasedItems_object
      //     ),
      //   }
      // );
      // ========= ORDER HISTORY (END) =========

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
