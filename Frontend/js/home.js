
// console.log("in home.js");
// console.log(sessionStorage.getItem("userId"));
// sessionStorage.setItem("userId", 1);
const homePage = Vue.createApp({
    data() {
        return {
            products: [],
            userId: sessionStorage.getItem("userId"),
            cartCount: "",
        };
    }, // data

    mounted() {
        console.log("-------In user mounted------");
        userId = this.userId;
        // retrieve products from the backend
        axios
            .get("http://127.0.0.1:5100/products")
            .then((response) => {
                console.log("hi");
                console.log(response.data[0]);
                // this.products = response.data;
                this.products = response.data["data"]["products"];
            })
            .catch((error) => {
                console.log(error);
            });

        // retrieve cart count from the backend
        axios
            .get('http://127.0.0.1:5200/get_cart_count/' + userId)
            .then((response) => {
                this.cartCount = response.data["cart_count"];})

        console.log("-------end user  mounted------");
    },

    computed: {
        // make a computed property for the cart count
        cartCount() {

            
        },
    },

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

        addToCart(productID) {
            console.log(productID);
            let qtyInput = document.getElementById("qty" + productID ).value;
            
            // Get the userId from sessionStorage
            let userId = this.userId;
            console.log("----------addToCart----------");
            console.log(userId);
            console.log(productID);
            console.log(qtyInput);

            // Set the modal body to show a loading spinner till a response is received
            document.getElementById("modal-body").innerHTML = `
            <div>
                <i class="fa fa-spinner fa-spin" style="font-size:48px;color:gray"></i>
                <h3>Adding item to cart...</h3>
            </div>`;

            // Make an axios post request to the buyItem microservice
            axios.post('http://127.0.0.1:5200/add_to_cart', {
                "userId": userId,
                "productId": productID,
                "qtyInput": qtyInput
            })
            .then(response => {
                console.log(response.data);
                // Handle the response as needed

                if (response.data["success"]) {
                    document.getElementById("modal-body").innerHTML = `
                    <div>
                        <i class="fa fa-check-circle" style="font-size:48px;color:green"></i>
                        <h3>Successfully added to cart!</h3>
                    </div>`

                    // Update the cart count
                    this.cartCount += 1;
                }
                else {
                    let error = response.data["error"];
                    document.getElementById("modal-body").innerHTML = `
                    <div>
                        <i class="fa fa-remove" style="font-size:48px;color:red"></i>
                        <h3>${error}</h3>
                    </div>`

                }
            })
            .catch(error => {
                console.log(error);
                // Handle the error as needed
            });
        },
    },
});

const vm = homePage.mount("#homePage");
