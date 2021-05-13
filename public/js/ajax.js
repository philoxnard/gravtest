// This file supports AJAX calls to the gravity server.

// Gravity Generic Command
var COMMAND_AJAX_TEST = "ajax_test"

// Blog commands
var COMMAND_BLOG_NEW_POST = "blog_new_post"
var COMMAND_BLOG_SUBMIT_DELETE = "blog_submit_delete"
var COMMAND_BLOG_SUBMIT_EDIT = "blog_submit_edit"

// Event Commands
var COMMAND_EVENT_ATTENDEE_CHECKIN = "event_attendee_checkin"
var COMMAND_EVENT_ATTENDEE_DELETE = "event_attendee_delete"
var COMMAND_EVENT_ATTENDEE_EDIT = "event_attendee_edit"
var COMMAND_EVENT_SUBMIT_DELETE = "event_submit_delete"
var COMMAND_EVENT_SUBMIT_EDIT = "event_submit_edit"
var COMMAND_EVENT_SUBMIT_NEW = "event_submit_new"
var COMMAND_EVENT_REGISTER = "event_register"

// Contacts Commands
var COMMAND_CONTACT_ADD = "contact_add"
var COMMAND_CONTACT_EDIT = "contact_edit"
var COMMAND_CONTACT_DELETE = "contact_delete"

// User Management Commands
var COMMAND_USER_ADD_NEW = "user_add_new"
var COMMAND_USER_DELETE = "user_delete"
var COMMAND_USER_EDIT = "user_edit"
var COMMAND_USER_EDIT_PASSWORD = "user_edit_password"
var COMMAND_USER_LOGOUT = "user_logout"
var COMMAND_USER_REGISTER = "user_register"
var COMMAND_USER_SET_PASSWORD = "user_set_password"

// Stripe Commands
var COMMAND_STRIPE_CHARGE = "stripe_charge_card"
var COMMAND_STRIPE_GET_KEYS = "stripe_get_keys"
var COMMAND_STRIPE_GET_SESSION = "stripe_get_session"


function testphil() {

	console.log('found')

	let message = {
		"msg_type" : "request",
		"command" : "read_file"
	}

	sendAjax( message )

}

function test_ajax() {

	let ajax_test_input = $("#ajax_test_input").val()

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_AJAX_TEST,
		"value" : ajax_test_input
	}

	sendAjax( message )
}

function sendAjax( message ) {

	message_request = JSON.stringify( message )

	// Sending AJAX Request to logout.
	$.ajax({
		type: 'POST',
		url: "/api",
		contentType: "application/json",
		data: message_request,
		// Fetch the stored token from localStorage and set in the header
		success: function(response) {
			console.log( "Got back a response from our AJAX request, response = " + JSON.stringify( response ) )

			parseMessage( response )
		},
		error: function(response) {
			console.log("got back an error")
		}
	});

}


// Parses message that are returned from the MTS server
// TODO: Need to have one parseMessage that both AJAX and Websocket responses call.
function parseMessage(responseMessage) {

	// TODO: How do we check the type so we could do the JSON.parse here instead of in
	//       the calling function?
	json = responseMessage

	if ( json != null && "command" in json ) {

		if ( json["command"] == COMMAND_AJAX_TEST ) {
			handleAjaxTest(json)

		} else if ( json["command"] == "read_file" ) {
			handlePhilTest(json)

		} else if ( json["command"] == COMMAND_BLOG_NEW_POST ) {
			handleAdminNewBlog(json)

		} else if ( json["command"] == COMMAND_BLOG_SUBMIT_EDIT ) {
			handleAdminBlogEdit(json)

		} else if ( json["command"] == COMMAND_BLOG_SUBMIT_DELETE ) {
			handleAdminBlogPostDelete(json)

		} else if ( json["command"] == COMMAND_CONTACT_ADD ) {
			handleAdminContactAdd(json)

		} else if ( json["command"] == COMMAND_CONTACT_EDIT ) {
			handleAdminContactEdit(json)

		} else if ( json["command"] == COMMAND_CONTACT_DELETE ) {
			handleAdminContactDelete(json)

		} else if ( json["command"] == COMMAND_EVENT_ATTENDEE_CHECKIN ) {
			handleAdminEventAttendeeCheckin(json)

		} else if ( json["command"] == COMMAND_EVENT_ATTENDEE_DELETE ) {
			handleAdminEventAttendeeDelete(json)

		} else if ( json["command"] == COMMAND_EVENT_ATTENDEE_EDIT ) {
			handleAdminEventAttendeeEdit(json)

		} else if( json["command"] == COMMAND_EVENT_REGISTER ) {
			handleAdminEventRegistration(json)

		} else if( json["command"] == COMMAND_EVENT_SUBMIT_NEW ) {
			handleAdminEventNew(json)

		} else if( json["command"] == COMMAND_EVENT_SUBMIT_DELETE ) {
			handleAdminEventDelete(json)

		} else if( json["command"] == COMMAND_EVENT_SUBMIT_EDIT ) {
			handleAdminEventDelete(json)

		} else if( json["command"] == COMMAND_STRIPE_GET_KEYS ) {
			handleAdminEventDelete(json)

		} else if( json["command"] == COMMAND_USER_ADD_NEW ) {
			handleUserAddNew(json)

		} else if( json["command"] == COMMAND_USER_DELETE ) {
			handleUserDelete(json)

		} else if( json["command"] == COMMAND_USER_EDIT ) {
			handleUserEdit(json)

		} else if( json["command"] == COMMAND_USER_EDIT_PASSWORD ) {
			handleUserEditPassword(json)

		}  else if( json["command"] == COMMAND_USER_LOGOUT ) {
			handleUserLogout(json)

		}
	}
}

function sendBlogNewPost(title, subtitle, text) {

	var r = confirm("Are you sure you want to submit your post?");
	if (r == false) {
	  return;
	}

	let blog_new_post_title = $("#blog_new_post_title").val()
	let blog_new_post_subtitle = $("#blog_new_post_subtitle").val()
	let blog_new_post_text = $("#blog_new_post_text").val()

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_BLOG_NEW_POST,
		"blog_item" : {
			"title" : blog_new_post_title,
			"subtitle" : blog_new_post_subtitle,
			"text" : blog_new_post_text
		}
	}

	sendAjax(message)
}

function submitBlogEdit() {

	let blog_edit_title = $("#blog_edit_post_title").val()
	let blog_edit_subtitle = $("#blog_edit_post_subtitle").val()
	let blog_edit_text = $("#blog_edit_post_text").val()
	let blog_edit_label = $("#blog_edit_label").val()

	blog_edit_label

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_BLOG_SUBMIT_EDIT,
		"blog_item" : {
			"title" : blog_edit_title,
			"label" : blog_edit_label,
			"subtitle" : blog_edit_subtitle,
			"text" : blog_edit_text
		}
	}

	sendAjax(message)
}

function submitBlogPostDeleteHandler(){

	let blog_label = $("#edit_event_label").val()

	submitBlogPostDelete( blog_label, "/events" )
}

function submitBlogPostDelete(blogLabel, redirectLocation) {

	console.log( "submitEventDelete: Deleting blog post " + blogLabel )

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_BLOG_SUBMIT_DELETE,
		"blog_item" : {
			"label" : blogLabel
		}
	}

	sendAjax( message )
}

// ***** Contact Functions *****
function submitContactAdd() {

	let contact_first_name = $("#first_name").val()
	let contact_last_name = $("#last_name").val()
	let contact_email = $("#email").val()
	let contact_phone = $("#phone").val()

	//let event_id = $("#event_id").val()
	//console.log("event id is " + event_id)

	let message = {
		"msg_type" : "request",
		"command" : "contact_add",
		"contact_info" : {
			"first_name" : contact_first_name,
			"last_name" : contact_last_name,
			"email" : contact_email,
			"phone" : contact_phone
		}
	}

	sendAjax( message )

}


// ***** Gravity Event Functions *****

function submitNewEvent(title, subtitle, text) {

	var r = confirm("Are you sure you want to submit this event?");
	if (r == false) {
	  return;
	}

	let event_new_title = $("#event_new_title").val()
	let event_new_location = $("#event_new_location").val()
	let event_new_datetime = $("#event_new_datetime").val()
	let event_new_description = $("#event_new_description").val()

	let message = {
		"msg_type" : "request",
		"command" : "event_submit_new",
		"event_item" : {
			"title" : event_new_title,
			"location" : event_new_location,
			"datetime" : event_new_datetime,
			"description" : event_new_description
		}
	}

	sendAjax( message )
}

function submitEventEdit(title, subtitle, text) {

	let event_edit_title = $("#event_edit_title").val()
	let event_edit_label = $("#event_edit_label").val()
	let event_edit_location = $("#event_edit_location").val()
	let event_edit_datetime = $("#event_edit_datetime").val()
	let event_edit_description = $("#event_edit_description").val()

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_EVENT_SUBMIT_EDIT,
		"event_item" : {
			"label" : event_edit_label,
			"title" : event_edit_title,
			"location" : event_edit_location,
			"datetime" : event_edit_datetime,
			"description" : event_edit_description
		}
	}

	sendAjax( message )
}

function submitEventRegistration(callback) {

	let registration_first_name = $("#first_name").val()
	let registration_last_name = $("#last_name").val()
	let registration_email = $("#email").val()

	let event_id = $("#event_id").val()
	console.log("event id is " + event_id)

	let message = {
		"msg_type" : "request",
		"command" : "event_register",
		"event_item" : {
			"id" : event_id,
		},
		"registration_info" : {
			"first_name" : registration_first_name,
			"last_name" : registration_first_name,
			"email" : registration_email
		}
	}

	sendAjax(message)
}


function submitEventDeleteHandler(){

	let event_label = $("#edit_event_label").val()

	submitEventDelete( event_label, "/events" )
}

function submitEventDelete(eventLabel, redirectLocation) {

	console.log( "submitEventDelete: Deleting event " + eventLabel )

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_EVENT_SUBMIT_DELETE,
		"event_item" : {
			"label" : eventLabel
		}
	}

	sendAjax( message )
}

// ***** Stripe ******

function getStripeKeys() {

	let ajax_test_input = $("#ajax_test_input").val()

	let message = {
		"msg_type" : "request",
		"command" : COMMAND_STRIPE_GET_KEYS
	}

	sendAjax(message)
}
