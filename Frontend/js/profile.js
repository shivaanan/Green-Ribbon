// Payment Form Validation
(function () {
    'use strict'
    window.addEventListener('load', function () {
      // Fetch all the forms we want to apply custom Bootstrap validation styles to
      var forms = document.getElementsByClassName('needs-validation')
  
      // Loop over them and prevent submission
      Array.prototype.filter.call(forms, function (form) {
        form.addEventListener('submit', function (event) {
          if (form.checkValidity() === false) {
            event.preventDefault()
            event.stopPropagation()
          }
  
          form.classList.add('was-validated')
        }, false)
      })
    }, false)
  })()

// Vue
const profilePage = Vue.createApp({
    data() {
        return {
            products: [],
            buyHistory: [],
            sellHistory: [],
            tempObj: null,
            userId: sessionStorage.getItem("userId"),
        };
    }, // data

    mounted() {
        console.log("-------In user mounted------");
        userId = this.userId;
        // retrieve all user listings
        axios
            .get("http://127.0.0.1:5002/products")
            .then((response) => {
                console.log("listings loaded");
                console.log(response.data[0]);
                // this.products = response.data["data"]["pro"];
                this.products = response.data["data"]["products"];

                this.products.sort((a, b) => {
                    return new Date(a.dateOfPost) - new Date(b.dateOfPost); // sort ascending
                  })
            })
            .catch((error) => {
                console.log(error);
            });
        // retrieve user bought history
        axios
            .get("http://127.0.0.1:5004/purchased/"+ userId)
            .then((response) => {
                console.log("purchased loaded");
                console.log(response.data[0]);
                this.buyHistory = response.data;
                this.buyHistory.sort((a, b) => {
                    return new Date(b.order_date) - new Date(a.order_date); // sort ascending
                  })
            })
            .catch((error) => {
                console.log(error);
            });
        // retrieve user sold history
        axios
            .get("http://127.0.0.1:5004/sold/"+ userId)
            .then((response) => {
                console.log("sold loaded");
                console.log(response.data[0]);
                this.sellHistory = response.data;
                this.sellHistory.sort((a, b) => {
                    return new Date(b.order_date) - new Date(a.order_date); // sort ascending
                  })
                console.log(this.sellHistory);
            })
            .catch((error) => {
                console.log(error);
            });
        
    },

    computed: {

        listingCount() {
            let count = 0;
            if (Array.isArray(this.products)) {
                for (const product of this.products) {
                  if (product.sellerID == this.userId) {
                    count++;
                  }
                }
              }
            return count;
          }, 
          
    },

    methods: {

        // Buyer send refund request------------------------------------------------------------------------
        returnItem(buyOrder) {   
            let orderID = buyOrder.orderID;
            let productID = buyOrder.productID;
            console.log(orderID);
            // Make an axios post request to the ReturnItem microservice
            axios.post('http://127.0.0.1:5300/return_item', {
                "orderID": orderID,
                "productID": productID,
            })
            .then(response => {
                console.log(response.data);
                // Handle the response as needed
                if (response.data["code"]==200) {
                    // Change text and disable button
                    let button = document.getElementById(buyOrder.orderID+buyOrder.itemName)
                    button.textContent = "Refund Requested";
                    button.disabled = true
                    alert("Refund requested");
                }
                else {
                    alert("Refund request failed. Please try again");
                }
            })
            .catch(error => {
                console.log(error);
            });
        },

        // Seller reject refund approval pt1-------------------------------------------------------------------
        acceptRefund(sellOrder) {   
            let orderID = sellOrder.orderID;
            let productID = sellOrder.productID;
            let decision = 'accept';
            this.tempObj = {
                            "dataObj": sellOrder,
                            "orderID": orderID,
                            "decision": decision,
                            "productID": productID
                            };
        },

        //Seller submit cc info to refund pt 2-------------------------------------------------------------------
            
        sendPayment() {
            // Make an axios post request to the ReturnItem microservice
            let cardNumberInput = document.getElementById("cardNumber").value;
            let expDateInput = document.getElementById("expDate").value;
            let [exp_month, exp_year] = expDateInput.split("/");
            let CVCInput = document.getElementById("CVC").value;
            let cardHolderName = document.getElementById("cardHolderName").value;

            let card_details = {
                                number: cardNumberInput,
                                exp_month: exp_month,
                                exp_year: exp_year,
                                cvc: CVCInput,
                                };

            this.tempObj.cardDetails = card_details;
            this.tempObj.cardName = cardHolderName;
            console.log('please');
            console.log(this.tempObj);

            axios.post('http://127.0.0.1:5300/refund_decision', this.tempObj)
            .then(response => {
                console.log(response.data);
                if (response.data["success"]) {
                    // Remove refund buttons
                    let approveButton = document.getElementById('approve'+sellOrder.orderID+sellOrder.itemName);
                    let rejectButton = document.getElementById('reject'+sellOrder.orderID+sellOrder.itemName);
                    approveButton.remove();
                    rejectButton.remove();
                    alert("Refund successful");
                }
                else {
                    alert("Refund failed. Please try again");
                }
            })
            .catch(error => {
                console.log(error);
            });
        },

        // Seller reject refund---------------------------------------------------------------------------------
        rejectRefund(sellOrder) {   
            let orderID = sellOrder.orderID;
            let productID = sellOrder.productID;
            let decision = 'reject';

            axios.post('http://127.0.0.1:5300/refund_decision', {
                "orderID": orderID,
                "decision": decision,
                "productID": productID
            })
            .then(response => {
                console.log(response.data);
                if (response.data["code"]==200) {
                    // Remove refund buttons 
                    let approveButton = document.getElementById('approve'+sellOrder.orderID+sellOrder.itemName);
                    let rejectButton = document.getElementById('reject'+sellOrder.orderID+sellOrder.itemName);
                    approveButton.remove();
                    rejectButton.remove();
                    alert("Refund rejected");
                }
                else {
                    alert("Refund rejection failed. Please try again");
                }
            })
            .catch(error => {
                console.log(error);
            });
        },

    },
});

const vm = profilePage.mount("#profilePage");
