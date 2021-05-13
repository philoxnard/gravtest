#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

MessageParser.py

"""

# **** Local Imports ****
from JsonFile import *   # We are using this to read JSON files, should rename and separate the class.
from JsonMessage import *
from JsonMessageCommands import *
from JsonSchemaHelper import *
from MessageHandlers import *
from UserManagement import *
from GravityCharge import *
from GravityConfiguration import *

ENFORCE_SCHEMA = True
ENFORCE_API_LOGIN = True

# Any commands that are listed here are protected and required an authenticated token to pass validation
#  before the command can execute.
AUTH_PROTECTED_COMMANDS = [ COMMAND_USER_ADD_NEW, COMMAND_USER_DELETE, COMMAND_USER_EDIT ]

class MessageParser():

	@staticmethod
	def parseMessage(message, options=None, logger=None):

		if PRINT_API_REQUEST_MESSAGES == True:
			print("Parsing message from client: %s" % message)

		# Create the MessageHandlers class
		message_handlers = MessageHandlers(JsonMessage)

		message_response = None

		try:
			message_json = json.loads(message)

			if ENFORCE_SCHEMA == True:
				if JsonSchemaHelper.validateMessageSchema( message_json ) == False:

					message_response = JsonMessage.createErrorMessage( "reply", "None", "Failed Message Schema" )
					return message_response

			if "command" not in message_json:
				"""
				We are expecting each message to have a command so we know what to do with it.  Otherwise return back a message
				to the client that we could not find the message object
				"""
				message_response = JsonMessage.createErrorMessage( "None", "Could not find command object in message" )
				return message_response

			else:

				command = message_json["command"]
				message_response = None

				# First check that the user is validated for any protected commands
				if ENFORCE_API_LOGIN == True:
					# Any commands that are in this list, the user must be logged in to execute.
					if command in AUTH_PROTECTED_COMMANDS:

						if options != None and "token" in options:
							token = options["token"]
						elif "token" in message_json:
							token = message_json["token"]
						else:
							reason = "Could not find token, cannot process message"
							logger.error( reason )
							message_response = JsonMessage.createErrorMessage( "reply", command, reason )
							return message_response

						if UserManagement.validateToken(token.strip()) == False:
							reason = "Token is invalid, cannot process message"
							logger.error( reason )
							message_response = JsonMessage.createErrorMessage( "reply", command, reason )
							return message_response

				# If we have come this far, the token validation passed or this message doesn't require auth validation.
				if command == COMMAND_AJAX_TEST:
					message_response = message_handlers.handleAjaxTest( message_json, message_response, logger )

				elif command == COMMAND_LOGOUT:
					message_response = message_handlers.handleUserLogout( message_json, options, logger )

				elif command == COMMAND_USER_REGISTER:
					message_response = message_handlers.handleUserRegister( message_json, logger )

				elif command == COMMAND_LOGIN:
					message_response = message_handlers.handleUserLogin( message_json, logger )

				elif command == COMMAND_BLOG_NEW_POST:
					message_response = message_handlers.handleSetBlogNewPost( message_json, logger )

				elif command == COMMAND_BLOG_SUBMIT_EDIT:
					message_response = message_handlers.handleBlogSubmitEdit( message_json, logger )

				elif command == COMMAND_BLOG_SUBMIT_DELETE:
					message_response = message_handlers.handleBlogSubmitDelete( message_json, logger )

				elif command == COMMAND_CONTACT_ADD:
					message_response = message_handlers.handleContactAdd( message_json, logger )

				elif command == COMMAND_CONTACT_EDIT:
					message_response = message_handlers.handleContactEdit( message_json, logger )

				elif command == COMMAND_CONTACT_DELETE:
					message_response = message_handlers.handleContactDelete( message_json, logger )

				elif command == COMMAND_EVENT_SUBMIT_DELETE:
					message_response = message_handlers.handleEventSubmitDelete( message_json, logger )

				elif command == COMMAND_EVENT_SUBMIT_EDIT:
					message_response = message_handlers.handleEventSubmitEdit( message_json, logger )

				elif command == COMMAND_EVENT_ATTENDEE_CHECKIN:
					message_response = message_handlers.handleEventAttendeeCheckIn( message_json, logger )

				elif command == COMMAND_EVENT_ATTENDEE_DELETE:
					message_response = message_handlers.handleEventAttendeeDelete( message_json, logger )

				elif command == COMMAND_EVENT_ATTENDEE_EDIT:
					message_response = message_handlers.handleEventAttendeeEdit( message_json, logger )

				elif command == COMMAND_EVENT_REGISTER:
					message_response = message_handlers.handleEventRegister( message_json, logger )

				elif command == COMMAND_EVENT_SUBMIT_NEW:
					message_response = message_handlers.handleEventSubmitNew( message_json, logger )

				elif command == COMMAND_STRIPE_CHARGE:
					message_response = message_handlers.handleStripeCharge( message_json, logger )

				elif command == COMMAND_STRIPE_GET_KEYS:
					message_response = message_handlers.handleStripeGetKeys( message_json, logger )
				
				elif command == COMMAND_STRIPE_GET_SESSION:
					message_response = message_handlers.handleStripeGetSession( message_json, logger )

				elif command == COMMAND_USER_ADD_NEW:
					message_response = message_handlers.handleUserAddNew( message_json, logger )

				elif command == COMMAND_USER_DELETE:
					message_response = message_handlers.handleUserDelete( message_json, logger )

				elif command == COMMAND_USER_EDIT:
					message_response = message_handlers.handleUserEdit( message_json, logger )

				elif command == COMMAND_USER_EDIT_PASSWORD:
					message_response = message_handlers.handleUserEditPassword( message_json, logger )

				elif command == COMMAND_USER_LOGOUT:
					message_response = message_handlers.handleUserLogout( message_json, logger )

				elif command == "read_file":
					message_response = message_handlers.handlePhilTest( message_json, logger)

				else:
					message_response = JsonMessage.createErrorMessage( "reply", "None", "Not find supported command" )

		except Exception as e:
			error = "parseMessage: e = %s" % e
			print(error)
			message_response = JsonMessage.createErrorMessage( "reply", "None", error )

		return message_response


if __name__ == '__main__':

	message = {}
	message["command"] = "ajax_test"
	message["value"] = "TEST!"
	message_response = MessageParser.parseMessage( json.dumps( message ) )
	print(json.dumps(message_response))