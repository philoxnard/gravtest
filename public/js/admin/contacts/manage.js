
$( ".contact_delete_button" ).click(function() {

    var email = $(this).data('email');

    var r = confirm( "Are you sure you want to delete contact " + email );
    if (r == true) {
        console.log( "Deleting contact with email " + email )
        contactDelete( email )
    } else {
        console.log( "Delete Contact Canceled" )
    }
});

// Since we just added new buttons to the DOM. Set their click handlers
$( ".contact_edit_button" ).click(function() {

    var email = $(this).data('email');
    var first_name = $(this).data('first_name');
    var last_name = $(this).data('last_name');
    var phone = $(this).data('phone');

    $('#modal_edit_email').val( email );
    $('#modal_edit_first_name').val( first_name );
    $('#modal_edit_last_name').val( last_name );
    $('#modal_edit_phone').val( phone );

    // Now show the modal
    $('#editContactModal').modal('toggle');

});