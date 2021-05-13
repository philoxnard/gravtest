
$( document ).ready(function() {

	// DOM ready
	$("#sign_in_button").on('click', function(event) {

		// This prevents a typical form submission, we are handling it with AJAX.
		event.preventDefault();

		username = $("#inputUsername").val();
		password = $("#inputPassword").val();

		// Hide the login alert incase it was showing
		$("#login_alert").hide();

		console.log("calling log_user_in")
		// Try to log the user in.
		log_user_in(username, password, "/admin")
	});

	// DOM ready
	$("#checkout_button").on('click', function(event) {

		// This prevents a typical form submission, we are handling it with AJAX.
		event.preventDefault();

		console.log("checkout_button clicked")
		redirectToCheckout('sku_FhIjURrq6C9lAL');
	});

});

/**
 * function that checks if the browser supports HTML5
 * local storage
 *
 * @returns {boolean}
 */
function supportsHTML5Storage() {
	try {
		return 'localStorage' in window && window['localStorage'] !== null;
	} catch (e) {
		return false;
	}
}

// Called when the user tries to submit form request for new user
$( "#registerNewUserButton" ).click(function(event) {

	console.log("registerNewUserButton: calling setAddNewUser");

	// This prevents a typical form submission, we are handling it with AJAX.
	event.preventDefault();

	// Before we submit the new user info to the server, do some basic checks on the information
	//  entered.
	const first_name = $("#register_first_name").val();
	const last_name = $("#register_last_name").val();
	const username = $("#register_email").val();

	const password = $("#register_password").val();
	const password_confirm = $("#register_password_confirm").val();

	if ( first_name == "" ) {
		alert( "Warning: Please fill in the first name." )
	} else if ( last_name == "" ) {
		alert( "Warning: Please fill in the last name." )
	} else if ( username == "" ) {
		alert( "Warning: Please fill in the username." )
	} else if ( password == "" ) {
		alert( "Warning: Please fill in the password." )
	} else if ( password_confirm == "" ) {
		alert( "Warning: Please fill in the password confirmation." )
	} else if ( password != password_confirm ) {
		alert( "Warning: Passwords do not match, please fix." )
	} else {
		console.log( "Calling registerNewUser, last_name = " + last_name )
		registerNewUser( first_name, last_name, username, password, password_confirm );
	}

});

// This function cleans up any temporary or persistent storage
//  we were using while we were logged in.
function cleanupSession() {

	// Remove the token we were using, it's no longer valid and re-direct back to login page.
	document.cookie = "token="
	localStorage.token = ""
	localStorage.username = "";

}

// This function sends an AJAX message to the server to add a user to the system.
function registerNewUser( first_name, last_name, username, password, password_confirm ) {

	// Clear any previous errors before we continue
	//clearError();

	var user_info = {}

	user_info["first_name"] = first_name
	user_info["last_name"] = last_name
	user_info["username"] = username
	user_info["password"] = password
	user_info["password_confirm"] = password_confirm

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_USER_REGISTER,
		"user_info" : user_info
	}

	console.log( JSON.stringify( message ) )
	// Before we send this, we have to convert it to a JSON string.
	message_request = JSON.stringify( message )

	// Sending AJAX Request to register
	$.ajax({
		type: 'POST',
		url: "/api",
		contentType: "application/json",
		data: message_request,
		// Fetch the stored token from localStorage and set in the header
		success: function(response) {

			let json = response;

			if ( "token" in json ) {
				// Store the token in localStorage incase we want to make an AJAX request and
				//  also insert it into the header as a cookie.
				localStorage.token = json["token"];
				document.cookie = "token=" + localStorage.token;

				// Store the username incase we need to use it.
				localStorage.username = username;

				// Redirect to the admin page.
				redirect_location = window.location.protocol + "//" + window.location.hostname + ":"  + window.location.port + "/admin";
				window.location = redirect_location;
			} else {
				console.log( "No Token found in response: " + JSON.stringify( response ) )

				if ( "error" in json && "reason" in json["error"] ) {
					$("#register_alert_message").html( json["error"]["reason"] )
					$("#register_alert").show();
				}
			}

		},
		error: function(response) {
			
			console.log("got back an error")
			console.log(response);
		}
	});
}

/* ********** Custom Login Code ********************/

function log_user_in(username, password, redirectLocation) {
	// Right now when we login, we are just passing username:password
	//  Then we are assuming that the server will respond with a JWT we
	//  can use for future requests.

	let user_login_info = {
		"username" : username,
		"password" : password
	}

	let login_json = {
		"msg_type" : "request",
		"command" : "login",
		user_login_info : user_login_info
	}

	message_request = JSON.stringify( login_json )

	// Sending AJAX Request to login
	$.ajax({
		type: 'POST',
		url: "/api",
		contentType: "application/json",
		data: message_request,
		// Fetch the stored token from localStorage and set in the header
		success: function(response) {

			let json = response;

			if ( "token" in json ) {
				// Store the token in localStorage incase we want to make an AJAX request and
				//  also insert it into the header as a cookie.
				localStorage.token = json["token"];
				document.cookie = "token=" + localStorage.token;

				// Store the username incase we need to use it.
				localStorage.username = username;

				// Redirect to the home page.
				window.location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + redirectLocation;
			} else {
				console.log( "No Token found in response: " + JSON.stringify( json ) )

				if ( "error" in json && "reason" in json["error"] ) {
					$("#login_alert_message").html( json["error"]["reason"] )
					$("#login_alert").show();
				}
			}

		},
		error: function(response) {

			console.log("got back an error")
			console.log(response);
		}
	});

}

/* ********** Custom Logout Code ********************/

function logoutHandler() {
	logout( "/login" )
}

// Logout deletes our token from the cookie and localStorage.  We also
//  send a message to the server to logout so it revokes our current token.
function logout(redirectLocation) {

	let logout_json = {
		"msg_type" : "request",
		"command" : "logout",
		"token" : localStorage.token
	}

	message_request = JSON.stringify( logout_json )

	// Sending AJAX Request to logout.
	$.ajax({
		type: 'POST',
		url: "/api",
		contentType: "application/json",
		data: message_request,
		// Fetch the stored token from localStorage and set in the header
		success: function(response) {

			cleanupSession();
			// Re-direct back to index because if we need to go to the login page, the server will re-direct use there.
			window.location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + redirectLocation;

		},
		error: function(response) {
			console.log("got back an error")

			// Still clean up our tokens even though we got an error, but this shouldn't happen.
			cleanupSession();
			window.location = window.location.protocol + "//" + window.location.hostname + ":" + window.location.port + redirectLocation;

		}
	});
}