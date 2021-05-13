
// main.js:  Entry point for the js code, when the DOM is ready, opens a websocket connection.
//
// --Patrick Farrell 12/1/2016

$(document).ready(function() {

	// Called when the user wants to change their password.  This is used on the Settings Page.
	$( "#changePasswordButton" ).click(function() {

		$('#modal_change_password_username').val( localStorage.username );

		$('#editUserPasswordModal').modal('toggle');
	});

	$( "#submitSettingsButton" ).click(function() {

		console.log("submitSettingsButton: calling setConfiguration")

		// We are going to pull out from the DOM what we want to submit as the new configuraiton
		//  The server should change the settings to this configuration but leave the other info the same.
		var retention_time = $("#retention_time").val();

		var jsonConfiguration = {
			"retention_time" : retention_time
		}

		setConfiguration(jsonConfiguration);

	});

	$( "#settingsSaveButton" ).click(function() {

		var username = $("#user_name_input").val();
		var password = $("#password_input").val();
		var password2 = $("#password_input2").val();

		// If the passwords match, then store the new password
		if ( password == password2 ) {

			console.log( "storing the new password" )
			saveNewUsernameAndPassword( username, password );
		}
	});


	// **** These handlers are for the admin/contacts/manage page ****
	$( "#submitEditContactButton" ).click(function() {

		console.log("inside contact edit button")
		// Right now we don't let you edit the username because it would be more
		//  work to manage which username we are changing, since we use it as the key.

		const email = $("#modal_edit_email").val();
		const new_first_name = $("#modal_edit_first_name").val();
		const new_last_name = $("#modal_edit_last_name").val();
		const new_phone = $("#modal_edit_phone").val();

		var contact_info = {};

		contact_info["email"] = email;
		contact_info["first_name"] = new_first_name;
		contact_info["last_name"] = new_last_name;
		contact_info["phone"] = new_phone;

		contactEdit( contact_info );
		clearAddUserModal();

	});

	// **** These Handlers are for the admin event and event registrations pages ****
	$( "#addNewEventAttendeeButton" ).click(function() {

		// Clear the modal of any infomation that could have been there.
		clearEventAttendeeModal();

		$('#newEventAttendeeModal').modal('toggle');

	});

	$( "#submitNewEventAttendeeButton" ).click(function() {

		// Right now we don't let you edit the username because it would be more
		//  work to manage which username we are changing, since we use it as the key.

		const email = $("#modal_email").val();
		const new_first_name = $("#modal_first_name").val();
		const new_last_name = $("#modal_last_name").val();

		let event_id = $("#event_id").val()
		console.log("event id is " + event_id)

		var registration_info = {};

		registration_info["email"] = email;
		registration_info["first_name"] = new_first_name;
		registration_info["last_name"] = new_last_name;

		eventAttendeeNew( registration_info, event_id );
		clearAddUserModal();

	});

	$( "#submitNewEventAttendeeButton" ).click(function() {

		// Right now we don't let you edit the username because it would be more
		//  work to manage which username we are changing, since we use it as the key.

		const email = $("#modal_email").val();
		const new_first_name = $("#modal_first_name").val();
		const new_last_name = $("#modal_last_name").val();

		let event_id = $("#event_id").val()
		console.log("event id is " + event_id)

		var registration_info = {};

		registration_info["email"] = email;
		registration_info["first_name"] = new_first_name;
		registration_info["last_name"] = new_last_name;

		eventAttendeeNew( registration_info, event_id );
		clearAddUserModal();

	});

	$( "#submitEventAttendeeEditButton" ).click(function() {

		// Right now we don't let you edit the username because it would be more
		//  work to manage which username we are changing, since we use it as the key.

		const email = $("#modal_edit_email").val();
		const new_first_name = $("#modal_edit_first_name").val();
		const new_last_name = $("#modal_edit_last_name").val();
		const new_phone = $("#modal_edit_phone").val();

		let event_id = $("#event_id").val()
		console.log("event id is " + event_id)

		var registration_info = {};

		registration_info["email"] = email;
		registration_info["first_name"] = new_first_name;
		registration_info["last_name"] = new_last_name;
		registration_info["phone"] = new_phone;

		eventAttendeeEdit( registration_info, event_id );
		//clearEventAttendeeEditModal();

	});




	// **** These handlers are for the users.html page ****
	$( "#addNewUserButton" ).click(function() {

		// Clear the modal of any infomation that could have been there.
		clearAddUserModal();

		$('#newUserModal').modal('toggle');

	});

	// Called when the user tries to submit form request for new user
	$( "#submitNewUserButton" ).click(function(event) {

		console.log("calling setAddNewUser");

		// Before we submit the new user info to the server, do some basic checks on the information
		//  entered.
		const modal_first_name = $("#modal_first_name").val();
		const modal_last_name = $("#modal_last_name").val();
		const modal_username = $("#modal_username").val();

		const modal_password = $("#modal_password").val();
		const modal_password_confirm = $("#modal_password_confirm").val();

		if ( modal_first_name == "" ) {
			alert( "Warning: Please fill in the first name." )
		} else if ( modal_last_name == "" ) {
			alert( "Warning: Please fill in the last name." )
		} else if ( modal_username == "" ) {
			alert( "Warning: Please fill in the username." )
		} else if ( modal_password == "" ) {
			alert( "Warning: Please fill in the password." )
		} else if ( modal_password_confirm == "" ) {
			alert( "Warning: Please fill in the password confirmation." )
		} else if ( modal_password != modal_password_confirm ) {
			alert( "Warning: Passwords do not match, please fix." )
		} else {
			$('#newUserModal').modal('hide');
			userAddNew();
		}

	});

	$( "#submitEditUserButton" ).click(function() {

		// Right now we don't let you edit the username because it would be more
		//  work to manage which username we are changing, since we use it as the key.

		const username = $("#modal_edit_username").val();
		const new_first_name = $("#modal_edit_first_name").val();
		const new_last_name = $("#modal_edit_last_name").val();

		var user_info = {};

		user_info["username"] = username;
		user_info["first_name"] = new_first_name;
		user_info["last_name"] = new_last_name;

		user_info["permissions"] = {};

		// Default everything to trued
		user_info["permissions"]["admin"] = true;
		user_info["permissions"]["web"] = true;

		if( $('#editAdminCheckBox').is(':checked') == false ) {
			user_info["permissions"]["admin"] = false;
		}

		console.log("checking if checked")
		if( $('#editWebCheckBox').is(':checked') == false ) {
			user_info["permissions"]["web"] = false;
		}

		userEdit( user_info );
		clearAddUserModal();

	});

	// This is used by both the "Managed User" page and the "Settings" page, since
	//  changing the password for any user is the same as changing the password for our current
	//  user.
	$( "#submitChangeUserPasswordButton" ).click(function() {

		const username = $("#modal_change_password_username").val();
		const modal_change_password = $("#modal_change_password").val();
		const modal_change_password_confirm = $("#modal_change_password_confirm").val();

		// First check if the two passwords are the same
		if( modal_change_password == undefined || modal_change_password == "" || 
						modal_change_password != modal_change_password_confirm ) {

			alert( "Passwords are not the same, please try again" )

		} else {
			console.log("calling submit change user password")
			var user_info = {}

			user_info["username"] = username;
			user_info["password"] = modal_change_password;
			user_info["password_confirm"] = modal_change_password_confirm;

			$('#modal_change_password_username').val( username );

			userPasswordEdit( user_info );

			// Now toggle the modal off.
			$('#editUserPasswordModal').modal('toggle');
		}
		clearEditUserPasswordModal();

	});

	// **** END admin/users/manage functions ****

	// **** These handlers are for the admin/contacts/manage page ****
	$( "#addNewContactButton" ).click(function() {

		// Clear the modal of any infomation that could have been there.
		//clearNewContactModal();

		$('#newContactModal').modal('toggle');

	});

	// Called when the user tries to submit form request for new contact
	$( "#submitNewContactButton" ).click(function(event) {

		console.log("calling setAddNewContact");

		// Before we submit the new user info to the server, do some basic checks on the information
		//  entered.
		const modal_first_name = $("#modal_first_name").val();
		const modal_last_name = $("#modal_last_name").val();
		const modal_email = $("#modal_email").val();
		const modal_phone = $("#modal_phone").val();

		if ( modal_first_name == "" ) {
			alert( "Warning: Please fill in the first name." )
		} else if ( modal_last_name == "" ) {
			alert( "Warning: Please fill in the last name." )
		} else if ( modal_email == "" ) {
			alert( "Warning: Please fill in the username." )
		} else {
			$('#newContactModal').modal('hide');

			contact_info = {}
			contact_info["email"] = modal_email;
			contact_info["first_name"] = modal_first_name;
			contact_info["last_name"] = modal_last_name;
			contact_info["phone"] = modal_phone;

			contactAdd(contact_info);
		}

	});

});

function clearAddUserModal() {

	$("#modal_username").val("");
	$("#modal_first_name").val("");
	$("#modal_last_name").val("");

	$("#modal_password").val("");
	$("#modal_password_confirm").val("");

}

function clearEventAttendeeModal() {

	$("#modal_email").val("");
	$("#modal_first_name").val("");
	$("#modal_last_name").val("");
	$("#modal_phone").val("");

}


function clearEditUserPasswordModal() {

	$("#modal_change_password").val("");
	$("#modal_change_password_confirm").val("");

}

function clearEditContactModal() {

	$("#modal_email").val("");
	$("#modal_first_name").val("");
	$("#modal_last_name").val("");

}
