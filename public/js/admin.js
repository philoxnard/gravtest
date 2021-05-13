
// **** Admin Event Registration Functions ****

function eventAttendeeNew(registrationInfo, eventId) {

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_EVENT_REGISTER,
		"event_item" : {
			"id" : eventId,
		},
		"registration_info" : registrationInfo
	}

	sendAjax(message)

}

function eventAttendeeCheckIn(registrationInfo, eventId) {

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_EVENT_ATTENDEE_CHECKIN,
		"event_item" : {
			"id" : eventId,
		},
		"registration_info" : registrationInfo
	}

	sendAjax(message)

}

function eventAttendeeDelete(registrationInfo, eventId) {

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_EVENT_ATTENDEE_DELETE,
		"event_item" : {
			"id" : eventId,
		},
		"registration_info" : registrationInfo
	}

	sendAjax(message)

}

function eventAttendeeEdit(registrationInfo, eventId) {

	console.log("eventAttendeeEdit")

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_EVENT_ATTENDEE_EDIT,
		"event_item" : {
			"id" : eventId,
		},
		"registration_info" : registrationInfo
	}

	sendAjax(message)

}

function userDelete(username) {

	var user_info = {};

	user_info["username"] = username;

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_USER_DELETE,
		"user_info" : user_info
	}

	sendAjax(message)
}

function userLogout(username) {

	var user_info = {};
	user_info["username"] = username;

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_USER_LOGOUT,
		"user_info" : user_info
	}

	sendAjax(message)

}

// This function sends a message to the server to add a user to the system.
function userAddNew() {
	// TODO: This function is tied to users.html.  Should make it generic and pass in an object

	// Clear any previous errors before we continue
	clearError();

	var user_info = {}

	user_info["username"] = $("#modal_username").val();
	user_info["first_name"] = $("#modal_first_name").val();
	user_info["last_name"] = $("#modal_last_name").val();
	user_info["password"] = $("#modal_password").val();
	user_info["password_confirm"] = $("#modal_password_confirm").val();

	user_info["permissions"] = {}

	// Default everything to true
	user_info["permissions"]["admin"] = true;
	user_info["permissions"]["web"] = true;

	if( $('#adminCheckBox').is(':checked') == false ) {
		user_info["permissions"]["admin"] = false;
	}

	if( $('#webCheckBox').is(':checked') == false ) {
		user_info["permissions"]["web"] = false;
	}

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_USER_ADD_NEW,
		"user_info" : user_info
	}

	sendAjax(message)

}

function userEdit(userInfo) {

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_USER_EDIT,
		"user_info" : userInfo
	}

	sendAjax(message)

}

// This function is called by a client that may want to change the
//  password for themselves or another user.  Must validate that they
//  have that permission on the server.
function userPasswordEdit(userInfo) {

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_USER_EDIT_PASSWORD,
		"user_info" : userInfo
	}

	sendAjax(message)

}

// ***** End User Functions *****

// ***** Start Contact Functions ******

// This function sends a message to the server to add a user to the system.
function contactAdd(contactInfo) {

	// Clear any previous errors before we continue
	//clearError();

	var contact_info = {}

	if ( "email" in contactInfo ) {
		contact_info["email"] = contactInfo["email"]
	} else {
		alert( "Email required" )
		return;
	}

	if ( "first_name" in contactInfo ) {
		contact_info["first_name"] = contactInfo["first_name"]
	}

	if ( "last_name" in contactInfo ) {
		contact_info["last_name"] = contactInfo["last_name"]
	}

	if ( "phone" in contactInfo ) {
		contact_info["phone"] = contactInfo["phone"]
	}

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_CONTACT_ADD,
		"contact_info" : contact_info
	}

	sendAjax(message)

}

function contactEdit(contactInfo) {

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_CONTACT_EDIT,
		"contact_info" : contactInfo
	}

	sendAjax(message)

}

function contactDelete(email) {

	var contact_info = {};

	contact_info["email"] = email;

	var message = {
		"msg_type" : "request",
		"command" : COMMAND_CONTACT_DELETE,
		"contact_info" : contact_info
	}

	sendAjax(message)

}

function clearError() {
	$("#errors").hide();
}