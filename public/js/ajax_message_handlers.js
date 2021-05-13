
function handleAjaxTest(json) {

	if ( "output" in json ) {
		$("#ajax_test_output").html( json["output"] )
	}

	$("div#ajax_output_alert").show()

}

function handlePhilTest(json) {
	let text = JSON.parse(json["file"])
	for (i=0; i<text.length; i++) {
		$("#filecontent").append(text[i] + "</br>")
	}
}

// **** Admin Blog Handlers ****

function handleAdminNewBlog(json) {

	alert ( "New blog post submitted" )
	window.location = "/admin/blog/manage";
}

function handleAdminBlogEdit(json) {

	alert ( "Edit event submitted" )
	window.location = "/admin/blog/manage";
}

function handleAdminBlogPostDelete(json) {

	alert ( "Delete event submitted" )

	location.reload();
}

// ***** Admin Contact Handlers *****

function handleAdminContactAdd(json) {

	location.reload();
}

function handleAdminContactDelete(json) {
	// TODO: Pull out the email and display which contact was deleted?

	console.log( "Success: Got back response that we deleted the contact" )
	location.reload();
}

function handleAdminContactEdit(json) {

	console.log( "Success: Got back response that we edited the user" )
	location.reload();
}

// ***** Admin Event Attendee Handlers *****

function handleAdminEventAttendeeCheckin(json) {

	location.reload();

}

function handleAdminEventAttendeeDelete(json) {

	console.log( "Success: Got back response that we deleted the event attendee" )
	location.reload();

}

function handleAdminEventAttendeeEdit(json) {

	location.reload();

}

// ***** Admin Event Handlers *****

function handleAdminEventDelete(json) {

	alert ( "Delete event submitted" )

	location.reload();
}

function handleAdminEventEdit(json) {

	alert ( "Edit event submitted" )

	//window.location = "/events";
}

function handleAdminEventNew(json) {

	alert ( "New event submitted" )

	window.location = "/admin/events/manage";
}

function handleAdminEventRegistration(json) {

	$('#eventRegisterModal').modal('hide');

	let event_id = $("#event_id").val()
	let event_label = $("#event_label").val()
	window.location = "/event/confirmed/" + event_label;
}

// **** User Handlers ****

function handleUserAddNew(json) {

	console.log( "Success: Got back response that we created a user" )
	location.reload();
}

function handleUserDelete(json) {

	console.log( "Success: Got back response that we deleted a user" )
	location.reload();
}

function handleUserEdit(json) {

	console.log( "Success: Got back response that we edited the user" )
	location.reload();
}

function handleUserEditPassword(json) {

	console.log( "Success: Got back response that we edited the user password" )
}

function handleUserLogout(json) {

	console.log( "Success: Got back response that we logged the user out" )
	location.reload();

}

// **** Stripe Handlers ****

function handleGetStripeKeys(json) {

	if ( "output" in response ) {
		localStorgage.sk_test = json["sk_test"]
	}

}