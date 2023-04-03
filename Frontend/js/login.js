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
	
	console.log("test signin button");
	
	let email = document.getElementById("username").value
	let password = document.getElementById("password").value

	console.log(email);
	console.log(password);

	console.log("-------In user signIn------");
        
	axios.post('http://127.0.0.1:5100/verify_login', {
		"email":  email,
		"password" : password
		})
		.then(response => {
			// console.log(response.data);
			let userId = response.data["data"]["userId"];
			
			// stores userId in session storage
			sessionStorage.setItem("userId", userId);
			console.log(sessionStorage.getItem("userId"));
			
			// Redirect to home page
			window.location.href = "home.html";

		})
		
		.catch(error => {
			// Show error message
			document.getElementById("error").innerHTML = "Invalid email or password";
			
		});
	console.log("-------end user signIn------");
}
// ---------------------------------------------------------------------------------


// -------------- sign up function  ------------------------------------------------
function signUp() {
	
	console.log("test signin button");
	
	let name = document.getElementById("newName").value
	let email = document.getElementById("newEmail").value
	let password = document.getElementById("newPassword").value

	console.log(email);
	console.log(password);

	console.log("-------In user signUp------");
        
	axios.post('http://127.0.0.1:5100/create_acct', {
		"newName" : name,
		"newEmail":  email,
		"newPassword" : password
		})
		.then(response => {
			// console.log(response.data);
			console.log(response.data["message"]);

			document.getElementById("creationStatus").innerHTML = "Creation successful, Please login using your credentials";
			
		})
		
		.catch(error => {
			console.log(error.response.data["message"]);
			document.getElementById("creationStatus").innerHTML = "Email exists!";
			
		});

		document.getElementById("newName").value = ""
		document.getElementById("newEmail").value = ""
		document.getElementById("newPassword").value = ""

	console.log("-------end user signUp------");
}
// ---------------------------------------------------------------------------------