document.addEventListener("DOMContentLoaded", function () {
  const checkoutButton = document.getElementById("checkout-button");
  checkoutButton.addEventListener("click", handleCheckout);

  // ======================== FUNCTION TO SHOW BUTTON LOADING (START) ========================
  function setLoadingState(loading) {
    if (loading) {
      checkoutButton.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Loading...`;
      checkoutButton.disabled = true;
    } else {
      checkoutButton.innerHTML = `Checkout`;
      checkoutButton.disabled = false;
    }
  }
  // ======================== FUNCTION TO SHOW BUTTON LOADING (END) ========================

  async function handleCheckout(event) {
    event.preventDefault();
    // =============== BUTTON WILL SHOW IT'S LOADING FOR 3 SECOND (START) ===============
    setLoadingState(true);
    setTimeout(() => {
      setLoadingState(false);
    }, 3000);
    // =============== BUTTON WILL SHOW IT'S LOADING FOR 3 SECOND (END) ===============

    const publicKey =
      "pk_test_51MltK7EBOpB8WMsEafwEYrSYcLFCnAasAwZceaxQYgfYrZCxiqFymPFqCAhtz4BL0L7XB1HwKWzK53blzlcakXAj00b5LtAwQQ"; // Replace with your Stripe public key

    const stripe = Stripe(publicKey);

    const cardNumberInput = document.getElementById("cardNumber").value;
    const expDateInput = document.getElementById("expDate").value;
    const [exp_month, exp_year] = expDateInput.split("/");
    const CVCInput = document.getElementById("CVC").value;

    card_details = {
      number: cardNumberInput,
      exp_month: exp_month,
      exp_year: exp_year,
      cvc: CVCInput,
    };
    console.log("sessionStorage (START)");
    console.log(sessionStorage);
    console.log("sessionStorage (END)");
    var userId = sessionStorage.getItem("userId");
    // console.log("WHEN CLICK CHECKOUT -- START");
    // console.log(userId);

    // Card Holder Name
    const cardHolderName = document.getElementById("cardHolderName").value;
    const combinedData = {
      userId: userId,
      // dataObj: jsonData,
      cardDetails: card_details,
      cardName: cardHolderName,
    };
    // console.log("TEST CARD (START)");
    // console.log(combinedData);
    // console.log(typeof combinedData);
    // console.log("TEST CARD (END)");

    const paymentResponse = await fetch("http://127.0.0.1:5200/buy_item", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(
        combinedData
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
    const data = await paymentResponse.json();
    console.log(data)
    // console.log("paymentResponse START")
    // console.log(data)
    // console.log("paymentResponse END")

    // const result = await stripe.confirmCardPayment(
    //   data.data.payment_result.clientSecret,
    //   {
    //     payment_method: {
    //       card: card,
    //       billing_details: {
    //         name: cardHolderName, // Replace with a form input for the user's name
    //       },
    //     },
    //   }
    // );

    if (data.code !== 201) {
      // PAYMENT FAILED
      const errorMessage = data['message'];
      console.error("Payment failed:", errorMessage);
      const errorMessageElement = document.getElementById("error-message");
      errorMessageElement.textContent = errorMessage;
      errorMessageElement.style.display = "block";
    } else {
      // PAYMENT SUCCESS
      console.log("Payment succeeded:", data.message);

      purchasedItems_string = data.data.payment_result.description;
      // console.log("TEST purchaseItems_string START")
      // console.log(purchasedItems_string)
      // console.log("TEST purchaseItems_string END")

      if (typeof purchasedItems_string === 'string') {
        purchasedItems_string = purchasedItems_string.replace(/'/g, '"');
        purchasedItems_object = JSON.parse(purchasedItems_string);
      } else{
        purchasedItems_object = purchasedItems_string
      }
      
      
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
    // ...
    // if (data.code != 201) {
    //   console.error("Payment failed:", data.message);
    //   errorMessageElement.textContent = data.message;
    //   errorMessageElement.style.display = "block";
    // } else {
    //   console.log("Payment succeeded:", data.message);
    //   errorMessageElement.style.display = "none";
    //   window.location.href = "thanks.html"; // Redirect to thanks.html after successful payment
    // }
  }
});
