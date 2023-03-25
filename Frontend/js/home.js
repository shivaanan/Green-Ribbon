

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
