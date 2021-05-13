
/*
  Written by J. Patrick Farrell
  Copyright 2019 Creative Collisions Technology, LLC

  This file has functions that handle the client side implementation
  of the Gravity Websocket protocol.

  Websockets are persistent connection between the client and the server once opened.
 */

// File 
let COMMAND_AJAX_TEST = "ajax_test"

function doConnect()
{
	console.log("doConnect");

	if ( location.protocol == "https:" ) {
		url = "wss://" + window.location.hostname + "/ws1.ws"
	} else {
		url = "ws://" + window.location.hostname + "/ws1.ws"
	}
	websocket = new WebSocket(url);

	websocket.onopen = function(evt) { onOpen(evt) };
	websocket.onclose = function(evt) { onClose(evt) };
	websocket.onmessage = function(evt) { onMessage(evt) };
	websocket.onerror = function(evt) { onError(evt) };
}

function checkWebSocketReady() {

	// Values that indicate state of the websocket
	// 0: CONNECTING, the connection is not open yet.
	// 1: OPEN, the connection is open and ready to communicate.
	// 2: CLOSING, the connection is in the process of closing.
	// 3: CLOSED, the connection is closed or couldn't be opened.
	if( typeof websocket == 'undefined' || websocket.readyState != WebSocket.OPEN ) {
		return false;
	}

	return true;	
}

function doDisconnect() {
	websocket.close()
}

function onOpen(evt)
{
	console.log("onOpen");
	enableInputFields();
}

function onClose(evt)
{
	console.log("onClose");
	disableInputFields();
}

function toggleWebSocket() {

	if ( checkWebSocketReady() == true ) {
		doDisconnect();
	} else {
		doConnect();
	}
}

function onError(evt)
{
	console.log("onError");
	showError("Could not connect to WebSocket server");
}

function onMessage(evt)
{
	console.log("response: " + evt.data + '\n');

	var json = JSON.parse(evt.data);

	// First check if there was an error in this message.
	if ( "error" in json ) {

		error = json["error"]

		if( "reason" in error ) {
			showError(error["reason"]);
		} else {
			console.log("Error: error message found but no reason")
		}
	}

	// Make sure we at least have command in this message otherwise fail.
	if ( "msg_type" in json == false ) {
		console.log("Error: command was not found in message, invalid and cannot continue")
		return;
	}

	command = json["command"]

	if ( json["msg_type"] == "reply" ) {

		parseMessage( json )
	}

}

function doSendJson(jsonMessage) {

	doSend(JSON.stringify( jsonMessage ));

}

function doSend(message)
{
	if (websocket.readyState === 1) {
		websocket.send(message);
	}
}

// Handles parsing the message and passing off to the correct handler.
function parseMessage(json) {

	if ( command == COMMAND_AJAX_TEST ) {
		handleAjaxTestResponse(json)
	}
}

// ****** Message Handlers *******
// These functions are called to handle a particular message that is received from
//  the user and update the view with the result.  These are the first level functions that
//  get called for a particular message.  There can be multiple helper functions below.
function handleAjaxTestResponse(json) {
	console.log( "handleAjaxTestResponse: receieved " + json )

	if ( "output" in json ) {
		$("#websocket_test_output").html( json["output"] )
	}

	$("div#websocket_output_alert").show()
}

// ******** End Message Handlers ********

// ****** Send Message Functions *******
function sendAjaxTest() {

	let websocket_test_input = $("#websocket_test_input").val()

	var message = {
		"msg_type" : "request",
		"command" : "ajax_test",
		"value" : websocket_test_input
	}

	doSendJson(message);
}

// ******** UI Helpers ********

function enableInputFields() {
	console.log("enableInputFields")

	$("#send_websocket_button").prop("disabled", false);
	$("#websocket_test_input").prop("disabled", false);

	$("#toggle_websocket_button").html('Close Websocket')
	
}

function disableInputFields() {
	$("#send_websocket_button").prop("disabled", true);
	$("#websocket_test_input").prop("disabled", true);

	$("#toggle_websocket_button").html('Open Websocket')

	$("div#websocket_output_alert").hide()
}

function showError(errorMessage) {
	$("#errors").show();
	$("#error_message").html(errorMessage);
}

function clearError() {
	$("#errors").hide();
}

