const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

function signIn() {
	document.getElementById("error").innerHTML = ""
	
	if (!validateSignIn()) {
		document.getElementById("error").innerHTML = "erorrr"
	}
}

function validateSignIn() {
	var username = document.getElementById("username").value;
	var pw = document.getElementById("password").value;
	console.log(username)

	if (username == "" || pw == "") {
		return false
	}
	return true

}