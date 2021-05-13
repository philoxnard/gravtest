
/*
This file enables file upload over AJAX.  By using Javascript to override
a form submission, you have more control over how the file upload over a POST
request is completed.
*/

var fileSelect = document.getElementById('file-select');

function uploadFiles() {

	event.preventDefault();

	// Get the selected files from the input.
	const fileupload = document.getElementById( "fileupload" )
	var files = fileupload.files;

	// Create a new FormData object.
	var formData = new FormData();

	// Loop through each of the selected files.
	for (var i = 0; i < files.length; i++) {

		var file = files[i];

		// Check the file type.
		//if ( !file.type.match('image.*') ) {
		//	continue;
		//}

		// Files
		formData.append(name, file, file.name);
	}

	// Set up the request.
	var xhr = new XMLHttpRequest();

	// Need to determine the URL based on if we are connected over HTTP or HTTPS
	var url = "";
	if (location.protocol != 'https:')
	{
		url = 'http://' + window.location.hostname;
	} else {
		url = 'https://' + window.location.hostname;
	}

	xhr.open( "POST", url )

	// Set up a handler for when the request finishes.
	xhr.onload = function () {

		if (xhr.status === 200) {
			console.log("file was uploaded and we got back a response");

			alert('The file was uploaded!');

		} else {
			alert('An error occurred!');
		}
	};

	// Send the Data.
	xhr.send(formData);

}