// Hide or show the password
document.getElementById("toggle_password").addEventListener("click", myFunction);

function myFunction() {
	this.toggleClass("fa-eye fa-eye-slash");
	var input = document.getElementById("password");
	if (input.attr("type") == "password") {
	    input.attr("type", "text");
	  } else {
	    input.attr("type", "password");
	  }
}
