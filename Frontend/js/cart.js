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


// console.log("in home.js");
// console.log(sessionStorage.getItem("userId"));

const cartPage = Vue.createApp({
    data() {
        return {
            cartItems: [],
            userId: sessionStorage.getItem("userId"),
            
        };
    }, // data

    mounted() {
        console.log("-------In user mounted------");
        let userId = this.userId;
        // retrieve products from the backend
        // need change -> extract from buyItem Complex microservice
        axios
            .get('http://127.0.0.1:5200/get_cart/' + userId)
            .then((response) => {
                let cart_list = response.data["data"]["cart_list"];
                this.cartItems =  cart_list;
            })
            
            .catch((error) => {
                console.log(error);
                let error_message = error.response.data["message"];
                console.log(error_message);
            });


        console.log("-------end user  mounted------");
    },

    computed: {
        
        subtotal() {
            
            var totalPrice = this.cartItems.map(function(item) {
                return item.price * item.inputQuantity;
              }).reduce(function(total, value) {
                return total + value;
              }, 0);
              
            return totalPrice;
        },

        gst(){
            return this.subtotal * 0.08;
        },

        grandTotal(){
            return this.subtotal + this.gst;
        }


        
    },

    methods: {

        removeItem(productID) {
            console.log("hi delete");

            let userId = this.userId;
            
            axios
            .delete('http://127.0.0.1:5200/delete_cart_item/' + userId + '/' + productID)
            .then((response) => {


                // Filter out the item with the specified ID
                var newCartItems = this.cartItems.filter(function(item) {
                  return item.productID !== productID;
                });
                
                // Update the cartItems array with the new array
                this.cartItems = newCartItems;


                document.getElementById("delete_alert").innerHTML = `
                    <div class="alert alert-warning" role="alert">
                        Removed item from cart!
                    </div>`
    
                    setTimeout(function() {
                        var alert = document.querySelector('.alert');
                        alert.parentNode.removeChild(alert);
                      }, 3000);
                
            })
            
            .catch((error) => {
    
            });
        },


    },
});

const vm = cartPage.mount("#cartPage");
