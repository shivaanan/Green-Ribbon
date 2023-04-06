// console.log("in home.js");
// console.log(sessionStorage.getItem("userId"));
// sessionStorage.setItem("userId", 1);
const homePage = Vue.createApp({
    data() {
        return {
            displayProducts: [],
            products: [],
            userId: sessionStorage.getItem("userId"),
            cartCount: "",
            distances: {},
            isLoading: true,
            
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
                // console.log(response.data[0]);
                // this.products = response.data;
                this.products = response.data["data"]["products"];
            })
            .catch((error) => {
                console.log(error);
            });



        // retrieve distance of the listings from the backend
        axios
        .get("http://127.0.0.1:5100/calculatedistance")
        .then((response) => {
            console.log("hi");
            // console.log(response.data[0]);
            // this.products = response.data;
            // console.log(this.products);
            // this.products = response.data["data"]["distances"];
            console.log(response.data["data"]["distances"]);
            this.distances = response.data["data"]["distances"];
            
            this.products.forEach((product) => {
                product.distance = this.distances[product.productID];
            });
            
            console.log(this.products);
            // clg(this.products);

            // sort products by distance
            this.products.sort((a, b) => {
                return a.distance - b.distance;
            });

            this.displayProducts = this.products;

            // set isLoading to false once products have loaded
            this.isLoading = false;
            
        })
        .catch((error) => {
            console.log(error);
        });

        // retrieve cart count from the backend
        axios
            .get('http://127.0.0.1:5200/get_cart/' + userId)
            .then((response) => {
                let cart_list = response.data["data"]["cart_list"];
                this.cartCount = cart_list.length;
            })

        console.log("-------end user  mounted------");
    },

    computed: {

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
            axios.post('http://127.0.0.1:5200/add_to_cart',
            {
                "userId": userId,
                "productID": productID,
                "qtyInput": qtyInput
            }
            // , {
            //     headers: {
            //         "Content-type": "application/json"
            //     }}
            )
            .then(response => {
                console.log(response.data);
                // Handle the response as needed

               
                document.getElementById("modal-body").innerHTML = `
                <div>
                    <i class="fa fa-check-circle" style="font-size:48px;color:green"></i>
                    <h3>Successfully added to cart!</h3>
                </div>`

                // Update the cart count
                this.cartCount += 1;
                
            })
            .catch(error => {
                // console.log(error);
                // console.log(error.response.data);
                // Handle the error as needed
                let error_message = error.response.data["message"];
                document.getElementById("modal-body").innerHTML = `
                <div>
                    <i class="fa fa-remove" style="font-size:48px;color:red"></i>
                    <h3>${error_message}</h3>
                </div>`
            });
        },
    },
});

const vm = homePage.mount("#homePage");