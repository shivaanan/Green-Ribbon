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
            .get('http://127.0.0.1:5100/get_cart/' + userId)
            .then((response) => {
                console.log(response.data);
                this.cartItems = response.data;
            })
            .catch((error) => {
                console.log(error);
            });


        console.log("-------end user  mounted------");
    },

    computed: {

        
    },

    methods: {


    },
});

const vm = cartPage.mount("#cartPage");
