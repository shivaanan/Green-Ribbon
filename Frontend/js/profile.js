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
                console.log("hi");
                console.log(response.data[0]);
                this.products = response.data;
                this.products.sort((a, b) => {
                    return new Date(a.dateOfPost) - new Date(b.dateOfPost); // sort ascending
                  })
            })
            .catch((error) => {
                console.log(error);
            });
        // retrieve user buy history
        axios
            .get("http://127.0.0.0:5004/purchased/"+ userId)
            .then((response) => {
                console.log(response.data[0]);
                this.buyHistory = response.data;
                this.buyHistory.sort((a, b) => {
                    return new Date(b.order_date) - new Date(a.order_date); // sort ascending
                  })
            })
            .catch((error) => {
                console.log(error);
            });
        // retrieve user buy history
        axios
            .get("http://127.0.0.0:5004/sold/"+ userId)
            .then((response) => {
                console.log(response.data[0]);
                this.sellHistory = response.data;
                this.sellHistory.sort((a, b) => {
                    return new Date(b.order_date) - new Date(a.order_date); // sort ascending
                  })
            })
            .catch((error) => {
                console.log(error);
            });
        
    },

    computed: {

        listingCount() {
            let count = 0;
            for (const product of this.products) {
              if (product.sellerID == this.userId) {
                count++;
              }
            }
            return count;
          }, 
          
    },

    methods: {

        // Buyer send refund request------------------------------------------------------------------------
        returnItem(buyOrder) {   
            let orderID = buyOrder.orderID;
            // Make an axios post request to the ReturnItem microservice
            axios.post('http://127.0.0.1:5300/return_item', {
                "orderID": orderID,
            })
            .then(response => {
                console.log(response.data);
                // Handle the response as needed
                if (response.data["success"]) {
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

        // Seller send refund approval-----------------------------------------------------------------------
        approveRefund(sellOrder) {   
            let orderID = sellOrder.orderID;
            let decision = 'accept';

            // Make an axios post request to the ReturnItem microservice
            axios.post('http://127.0.0.1:5300/refund_decision', {
                "orderID": orderID,
                "decision": decision
            })
            .then(response => {
                console.log(response.data);
                // Remove refund buttons 
                if (response.data["success"]) {
                    let approveButton = document.getElementById('approve'+sellOrder.orderID+sellOrder.itemName);
                    let rejectButton = document.getElementById('approve'+sellOrder.orderID+sellOrder.itemName);
                    approveButton.remove();
                    rejectButton.remove();
                    alert("Refund allowed");
                }
                else {
                    alert("Refund failed. Please try again");
                }
            })
            .catch(error => {
                console.log(error);
            });
        },

        // Seller reject refund approval pt1-------------------------------------------------------------------
        rejectRefund(sellOrder) {   
            let orderID = sellOrder.orderID;
            let decision = 'reject';
            this.tempObj = {
                            "shippingCart": sellOrder,
                            "orderID": orderID,
                            "decision": decision
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
            console.log(tempObj);

            axios.post('http://127.0.0.1:5300/refund_decision', this.tempObj)
            .then(response => {
                console.log(response.data);
                // Remove refund buttons
                if (response.data["success"]) {
                    let approveButton = document.getElementById('approve'+sellOrder.orderID+sellOrder.itemName);
                    let rejectButton = document.getElementById('approve'+sellOrder.orderID+sellOrder.itemName);
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
