$( ".user_delete_button" ).click(function() {

    var username = $(this).data('username');

    var r = confirm( "Are you sure you want to delete user " + username );
    if (r == true) {
        console.log( "Deleting user " + username )
        userDelete( username )
    } else {
        console.log( "Delete User Canceled" )
    }
});

// Since we just added new buttons to the DOM. Set their click handlers
$( ".user_edit_button" ).click(function() {

    var username = $(this).data('username');
    var first_name = $(this).data('first_name');
    var last_name = $(this).data('last_name');

    var admin = $(this).data('admin');
    var web = $(this).data('web');

    $('#modal_edit_username').val( username );
    $('#modal_edit_first_name').val( first_name );
    $('#modal_edit_last_name').val( last_name );
    $('#modal_edit_first_name').val( first_name );
    $('#modal_edit_last_name').val( last_name );

    // Set checkboxes
    if ( admin == "True" ) {
        document.getElementById("editAdminCheckBox").checked = true;
    } else if ( admin == "False" ) {
        document.getElementById("editAdminCheckBox").checked = false;
    }

    if ( web == "True" ) {
        document.getElementById("editWebCheckBox").checked = true;
    } else if ( web == "False" ) {
        document.getElementById("editWebCheckBox").checked = false;
    }

    // Now show the modal
    $('#editUserModal').modal('toggle');

    });

$( ".user_logout_button" ).click(function() {

    var username = $(this).data('username');

    var r = confirm( "Are you sure you want to logout user " + username );
    if (r == true) {
        userLogout( username )
        console.log( "Logging out user " + username )
    } else {
        console.log( "User Logout Canceled" )
    }
});

$( ".user_set_password_button" ).click(function() {

    var username = $(this).data('username');

    $('#modal_change_password_username').val( username );

    $('#editUserPasswordModal').modal('toggle');

});