

const homePage = Vue.createApp({
    data() {
        return {
            products: [],
        };
    }, // data

    mounted() {
        console.log("-------In user mounted------");

        axios
            .get("http://127.0.0.1:5001/products")
            .then((response) => {
                console.log("hi");
                console.log(response.data[0]);
                this.products = response.data;
            })
            .catch((error) => {
                console.log(error);
            });

        console.log("-------end user  mounted------");
    },

    computed: {},

    methods: {
        async buyNow(productID) {
            console.log(productID);

            try {
                const response = await axios.post(
                    "http://127.0.0.1:5001/create-checkout-session",
                    {
                        product_id: productID,
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
        },

        incrementQuantity(productID) {
            let qtyInput = document.getElementById(productID ).value;
    
            qtyInput = parseInt(qtyInput) + 1;

            document.getElementById(productID).value = qtyInput;
        },   

        decrementQuantity(productID) {
            let qtyInput = document.getElementById(productID ).value;
         
            if (parseInt(qtyInput) == 0) {
                return;
            }

            qtyInput = parseInt(qtyInput) - 1;

            document.getElementById(productID).value = qtyInput;
        },   
    },
});

const vm = homePage.mount("#homePage");
