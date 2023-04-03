
// console.log("in home.js");
// console.log(sessionStorage.getItem("userId"));

const profilePage = Vue.createApp({
    data() {
        return {
            products: [],
            buyHistory: [],
            sellHistory: [],
            userId: 0,
            // userId: sessionStorage.getItem("userId"),
        };
    }, // data

    mounted() {
        console.log("-------In user mounted------");
        userId = this.userId;
        // retrieve all user listings
        axios
            .get("http://127.0.0.1:5001/products")
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
        // getAllHistorySorted() {
        //     return [...this.buyHistory, ...this.sellHistory].sort((a, b) => {
        //         return new Date(b.order_date) - new Date(a.order_date); // sort ascending
        //         })

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
//--------------------------------------------------------------------------------
        returnItem() {   
            let orderID = this.orderID;
            // Make an axios post request to the ReturnItem microservice
            axios.post('http://127.0.0.1:5200/return_item', {
                "orderID": orderID,
            })
            .then(response => {
                console.log(response.data);
                // Handle the response as needed

                if (response.data["success"]) {
                    //not sure how to give each button a unique ID
                    button.textContent = 'Requested';
                }
                else {
                    //idk pray?
                }
            })
            .catch(error => {
                console.log(error);
                // Handle the error as needed
            });
        },

        approveRefund() {   
            let orderID = this.orderID;
            let decision = 'accept'
            //Where do I pluck the dataObj from?

            // Make an axios post request to the ReturnItem microservice
            axios.post('http://127.0.0.1:5200/refund_decision', {
                "orderID": orderID,
                "decision": decision
            })
            .then(response => {
                console.log(response.data);
                // Handle the response as needed

                if (response.data["success"]) {
                    //not sure how to give each button a unique ID
                    button.textContent = 'Requested';
                }
                else {
                    //idk pray?
                }
            })
            .catch(error => {
                console.log(error);
                // Handle the error as needed
            });
        },



    },
});

const vm = profilePage.mount("#profilePage");
