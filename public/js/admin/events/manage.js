
$( ".attendee_delete_button" ).click(function() {

    var email = $(this).data('email');

    let event_id = $("#event_id").val()
    console.log("event id is " + event_id)

    let registration_info = {}
    registration_info["email"] = email;

    var r = confirm( "Are you sure you want to delete this attendee " + email );
    if (r == true) {
        console.log( "Deleting event attendee with email " + email )
        eventAttendeeDelete( registration_info, event_id )
    } else {
        console.log( "Delete Contact Canceled" )
    }
});

$( ".attendee_checkin_button" ).click(function() {

    var email = $(this).data('email');

    var registration_info = {}
    registration_info["email"] = email;

    let event_id = $("#event_id").val()
    console.log("event id is " + event_id)

    console.log("pressed attendee_checkin_button button")

    eventAttendeeCheckIn( registration_info, event_id );

});

$( ".attendee_edit_button" ).click(function() {

    console.log("pressed attendee_checkin_button button")

    var email = $(this).data('email');
    var first_name = $(this).data('first_name');
    var last_name = $(this).data('last_name');
    var phone = $(this).data('phone');

    $('#modal_edit_email').val( email );
    $('#modal_edit_first_name').val( first_name );
    $('#modal_edit_last_name').val( last_name );
    $('#modal_edit_phone').val( phone );

    $('#eventAttendeeEditModal').modal('toggle');
});