// -------------- Shifting between sign in and sign up tab -------------------------
const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
// ---------------------------------------------------------------------------------


// -------------- sign in function  ------------------------------------------------
 function signIn() {
	// document.getElementById("error").innerHTML = ""
	console.log("test signin button");
	
	let email = document.getElementById("username").value
	let password = document.getElementById("password").value

	console.log(email);
	console.log(password);

	console.log("-------In user signIn------");
        
	axios.post('http://127.0.0.1:5000/loginuser', {
		"email":  email,
		"password" : password
		})
		.then(response => {
			// console.log(response.data);
			console.log(response.data["success"]);

			if (response.data["success"]) {
				// Redirect to home page
				window.location.href = "home.html";
			  } else {
				// Show error message
				document.getElementById("error").innerHTML = "Invalid email or password";
			  }
			
		})
		
		.catch(error => {
			
		});

	console.log("-------end user signIn------");
}
// ---------------------------------------------------------------------------------


