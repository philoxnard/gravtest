#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

MessageHandlers.py

These are the message handlers that take care of JSON requests coming in.

Note: We had to create this as a class and pass in JsonMessage on purpose
because we cannot import JsonMessage because it doesn't work.

"""

# **** Local Imports ****
from GravityBlog import *
from GravityCharge import *
from GravityContacts import *
from GravityEvents import *
from JsonMessageCommands import *
from UserManagement import *

MSG_TYPE_REPLY = "reply"

class MessageHandlers():

	def __init__(self, JsonMessage):
		self.json_message = JsonMessage

	def handleAjaxTest(self, messageJson, messageResponse, logger=None):

		message_response = self.json_message.createResponseMessage( COMMAND_AJAX_TEST )

		if "value" in messageJson:
			value = messageJson["value"]
			output = "Gravity Server Received Input: %s" % value
			message_response["output"] = output

		return message_response

	# **** Blog Handlers ****

	def handleSetBlogNewPost(self, messageJson, logger):
		"""
		This function handles create a new blog entry in the blog system.
		"""

		message_response = self.json_message.createResponseMessage( COMMAND_BLOG_NEW_POST )

		if "blog_item" in messageJson:

			blog_item = messageJson["blog_item"]

			title = blog_item["title"]
			subtitle = blog_item["subtitle"]
			text = blog_item["text"]

			gravity_blog = GravityBlog()
			result = gravity_blog.createPost( title, subtitle, text )

			if result == None:
				error_reason = "handleSetBlogNewPost: Error creating new blog entry"
				logger.error( error_reason )
				message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_NEW_POST, error_reason )

		else:
			error_reason = "handleSetBlogNewPost: blog_item object not found"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_NEW_POST, error_reason )

		return message_response

	def handleBlogSubmitEdit(self, messageJson, logger):
		"""
		Handles submission of a blog edit.
		"""

		message_response = self.json_message.createResponseMessage( COMMAND_BLOG_SUBMIT_EDIT )

		if "blog_item" in messageJson:

			blog_item = messageJson["blog_item"]

			gravity_blog = GravityBlog()
			result = gravity_blog.editPost( blog_item )

			if result == None:
				error_reason = "handleBlogSubmitEdit: Error creating new blog entry"
				logger.error( error_reason )
				message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_SUBMIT_EDIT, error_reason )

		else:
			error_reason = "handleBlogSubmitEdit: blog_item object not found"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_SUBMIT_EDIT, error_reason )

		return message_response

	def handleBlogSubmitDelete(self, messageJson, logger):
		"""
		This function handles editing an event.
		"""

		message_response = self.json_message.createResponseMessage( COMMAND_BLOG_SUBMIT_DELETE )

		if "blog_item" in messageJson:

			blog_item = messageJson["blog_item"]

			if "label" not in blog_item:
				error_reason = "handleBlogSubmitDelete: Error blog label not found"
				logger.error( error_reason )
				message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_SUBMIT_DELETE, error_reason )
			else:

				blog_label = blog_item["label"]

				gravity_blog = GravityBlog()
				result = gravity_blog.deletePost( blog_label )

				if result == None:
					error_reason = "handleBlogSubmitDelete: Error submitting delete blog post"
					logger.error( error_reason )
					message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_SUBMIT_DELETE, error_reason )

		else:
			error_reason = "handleBlogSubmitDelete: event_item object not found"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", COMMAND_BLOG_SUBMIT_DELETE, error_reason )

		return message_response

	# **** Contact Handlers *****
	def handleContactAdd(self, messageJson, logger):
		"""
		Handles adding a contact to the list.

		If there is a "contact_list_info" object present, it uses this information
		to add the contact to a particular list.
		"""

		message_response = self.json_message.createResponseMessage( COMMAND_CONTACT_ADD )

		gravity_contacts = GravityContacts()

		if "contact_info" not in messageJson:
			error_reason = "handleContactAdd: Error cannot create new contact, contact_info not present"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", COMMAND_CONTACT_ADD, error_reason )

		if "contact_list_info" in messageJson:
			result, reason = gravity_contacts.contactAdd( messageJson["contact_info"], messageJson["contact_list_info"] )
		else:
			result, reason = gravity_contacts.contactAdd( messageJson["contact_info"] )

		if result == False or result == None:
			error_reason = reason
			logger.error( reason )
			message_response = self.json_message.createErrorMessage( "reply", COMMAND_CONTACT_ADD, reason )

		message_response["contact_info"] = messageJson["contact_info"]

		if "contact_list_info" in messageJson:
			message_response["contact_list_info"] = messageJson["contact_list_info"]

		return message_response


	def handleContactEdit(self, messageJson, logger):
		"""
		This function edits a contact in the system.
		"""
		command = COMMAND_CONTACT_EDIT

		if "contact_info" in messageJson:

			contact_info = messageJson["contact_info"]

			# Store the new user in the system.
			gravity_contacts = GravityContacts()
			contact_info_edit_confirmed = gravity_contacts.contactEdit( contact_info )

			if contact_info_edit_confirmed != None:
				logger.info( "Contact information edited successfully for %s" % contact_info["email"] )

				# Success in editing a contact, create a response
				message_response = self.json_message.createResponseMessage(command)
				message_response["contact_info"] = contact_info_edit_confirmed
			else:
				# Tell the user we couldn't find the user to delete
				error_message =  "We could not edit user %s" % contact_info["email"]
				logger.error( error_message )
				message_response = self.json_message.createErrorMessage( "reply", command, error_message )

		else:
			error_message =  "We could not find contact_info object"
			logger.error( error_message )
			message_response = self.json_message.createErrorMessage( "reply", command, error_message  )

		return message_response

	def handleContactDelete(self, messageJson, logger):
		"""
		This function edits a contact in the system.
		"""
		command = COMMAND_CONTACT_DELETE
		message_response = self.json_message.createResponseMessage(command)

		if "contact_info" in messageJson:

			contact_info = messageJson["contact_info"]

			# Store the new user in the system.
			gravity_contacts = GravityContacts()
			contact_info_delete_result, reason = gravity_contacts.contactDelete( contact_info )

			if contact_info_delete_result != None:
				logger.info( "Contact deleted successfully for %s" % contact_info["email"] )

				# Success in editing a contact, create a response
				message_response["contact_info"] = contact_info
			else:
				# Tell the user we couldn't find the user to delete
				error_message =  "We could not edit user %s" % contact_info["email"]
				logger.error( error_message )
				message_response = self.json_message.createErrorMessage( "reply", command, error_message )

		else:
			error_message =  "We could not find contact_info object"
			logger.error( error_message )
			message_response = self.json_message.createErrorMessage( "reply", command, error_message  )

		return message_response

	# **** Event Handlers *****

	def handleEventAttendeeCheckIn(self, messageJson, logger):
		"""
		This is the message handler for checking in an event attendee that has already
		registered for the event.
		"""

		command = COMMAND_EVENT_ATTENDEE_CHECKIN
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" in messageJson and "registration_info" in messageJson:

			event_item = messageJson["event_item"]
			registration_info = messageJson["registration_info"]

			gravity_events = GravityEvents()
			result, reason = gravity_events.eventAttendeeCheckIn( event_item, registration_info )

		return message_response

	def handleEventAttendeeDelete(self, messageJson, logger):
		"""
		This is the message handler that handles deleting an attendee that is registered for
		a particular event.
		"""

		command = COMMAND_EVENT_ATTENDEE_DELETE
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" in messageJson and "registration_info" in messageJson:

			event_item = messageJson["event_item"]
			registration_info = messageJson["registration_info"]

			gravity_events = GravityEvents()
			result, reason = gravity_events.eventAttendeeDelete( event_item, registration_info )
	
		return message_response

	def handleEventAttendeeEdit(self, messageJson, logger):
		"""
		This is the message handler that handles editing an attendee that is registered for
		a particular event.
		"""

		command = COMMAND_EVENT_ATTENDEE_EDIT
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" in messageJson and "registration_info" in messageJson:

			event_item = messageJson["event_item"]
			registration_info = messageJson["registration_info"]

			gravity_events = GravityEvents()
			result, reason = gravity_events.eventAttendeeEdit( event_item, registration_info )

		return message_response

	def handleEventRegister(self, messageJson, logger):
		"""
		Handles a user registering for the event.

		TODO: This should be more robust and not necessarily just pass event_item directly from the client.
		"""

		command = COMMAND_EVENT_REGISTER
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" not in messageJson:
			print("error we need an event item")

		if "registration_info" not in messageJson:
			print("error we need a registration info object")

		event_item = messageJson["event_item"]
		registration_info = messageJson["registration_info"]

		gravity_events = GravityEvents()
		result, reason = gravity_events.eventRegister( event_item, registration_info )

		if result == None:
			error_reason = "handleEventRegister: Error submitting event registration"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		# This registration did not complete, send the user the reason
		if result == False:
			message_response["warning"] = reason
		else:
			# Place the registration info in the response message.
			message_response["registration_info"] = registration_info

		return message_response


	def handleEventSubmitNew(self, messageJson, logger):
		"""
		This function handles create a new blog entry in the blog system.
		"""

		command = COMMAND_EVENT_SUBMIT_NEW
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" in messageJson:

			event_item = messageJson["event_item"]

			# TODO: Check for items.
			title = event_item["title"]
			location = event_item["location"]
			datetime = event_item["datetime"]
			description = event_item["description"]

			gravity_events = GravityEvents()
			print("calling createEvent with title %s" % title)
			result = gravity_events.createEvent( title, datetime, location, description )

			if result == None:
				error_reason = "handleSubmitNewEvent: Error submitting new event"
				logger.error( error_reason )
				message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		else:
			error_reason = "handleSubmitNewEvent: blog_item object not found"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		return message_response

	def handleEventSubmitEdit(self, messageJson, logger):
		"""
		This function handles editing an event.
		"""

		command = COMMAND_EVENT_SUBMIT_EDIT
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" in messageJson:

			event_item = messageJson["event_item"]

			gravity_events = GravityEvents()
			result = gravity_events.editEvent( event_item )

			if result == None:
				error_reason = "handleEventSubmiEdit: Error submitting new event"
				logger.error( error_reason )
				message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		else:
			error_reason = "handleEventSubmiEdit: event_item object not found"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		return message_response

	def handleEventSubmitDelete(self, messageJson, logger):
		"""
		This function handles editing an event.
		"""

		command = COMMAND_EVENT_SUBMIT_DELETE
		message_response = self.json_message.createResponseMessage( command )

		if "event_item" in messageJson:

			event_item = messageJson["event_item"]

			if "label" not in event_item:
				error_reason = "handleEventSubmitDelete: Error event label not found"
				logger.error( error_reason )
				message_response = self.json_message.createErrorMessage( "reply", command, error_reason )
			else:

				event_label = event_item["label"]

				gravity_events = GravityEvents()
				result = gravity_events.deleteEvent( event_label )

				if result == None:
					error_reason = "handleEventSubmitDelete: Error submitting delete event"
					logger.error( error_reason )
					message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		else:
			error_reason = "handleEventSubmitDelete: event_item object not found"
			logger.error( error_reason )
			message_response = self.json_message.createErrorMessage( "reply", command, error_reason )

		return message_response

	# **** User Management Functions ****
	def handleUserAddNew(self, messageJson, logger):
		"""
		This function takes in a message that sets a new user into the system.

		"""
		command = COMMAND_USER_ADD_NEW

		if "user_info" in messageJson:

			user_info = messageJson["user_info"]
			password_hold = user_info["password"]

			# TODO: Make sure the new user object matches the JSON schema.

			if "username" not in user_info or "password" not in user_info or "first_name" not in user_info or "last_name" not in user_info:
				message_response = self.json_message.createErrorMessage( "reply", command, "Warning: Incomplete information, cannot add new user" )
				return message_response

			# Store the new user in the system.
			user_info_confirmed, reason = UserManagement.addNewUser( user_info )

			if user_info_confirmed != None:
				logger.info( "Successfully created new user %s %s (%s)" % ( user_info["first_name"], user_info["last_name"], user_info["username"] ) )
				# Success in adding a user, create a response
				message_response = self.json_message.createResponseMessage(command)
				message_response["user_info"] = user_info_confirmed

				# Now that we have added a new user, let's log them in.
				# TODO: This should only happen if registering, not creating a user through the admin.
				result, token = UserManagement.verifyAndLoginUser( user_info["username"], password_hold )

				if result == True:
					message_response["token"] = token
				else:
					logger.error( "handleUserAddNew: This is strange and shouldn't happen, we just added a new user but we can't log them in" )
			else:
				logger.error( reason )
				# TODO: Add the right reason, passwords don't match or we already have this user.
				message_response = self.json_message.createErrorMessage( "reply", command, reason )

			return message_response

	def handleUserDelete(self, messageJson, logger):
		"""
		This function deletes a user if the user is present in the system
		"""
		command = "user_delete"

		if "user_info" in messageJson:

			user_info = messageJson["user_info"]

			# Store the new user in the system.
			user_info_delete_confirmed = UserManagement.deleteUser( user_info )

			if user_info_delete_confirmed != None:
				logger.info( "Successfully deleted user %s" % user_info["username"] )
				# Success in adding a user, create a response
				message_response = self.json_message.createResponseMessage(command)
				message_response["user_info"] = user_info_delete_confirmed
			else:
				# Tell the user we couldn't find the user to delete
				logger.info( "Failed to delete user" )
				message_response = self.json_message.createErrorMessage( command, "Warning: We could not delete user %s" % user_info["username"] )

		else:
			message_response = self.json_message.createErrorMessage( command, "Warning: We could not find user_info object" )

		return message_response

	def handleUserEdit(self, messageJson, logger):
		"""
		This function edits a user in the system.  Pass in a user_info object with the username and any new information.

		Currently you cannot change the username, to do this, just create a new user.  If required, could add.
		"""
		command = COMMAND_USER_EDIT

		if "user_info" in messageJson:

			user_info = messageJson["user_info"]

			# Store the new user in the system.
			user_info_edit_confirmed = UserManagement.editUser( user_info )

			if user_info_edit_confirmed != None:
				logger.info( "User information edited successfully for %s" % user_info["username"] )
				# Success in adding a user, create a response
				message_response = self.json_message.createResponseMessage(command)
				message_response["user_info"] = user_info_edit_confirmed
			else:
				# Tell the user we couldn't find the user to delete
				error_message =  "We could not delete user %s" % user_info["username"]
				logger.error( error_message )
				message_response = self.json_message.createErrorMessage( command, error_message )

		else:
			error_message =  "We could not find user_info object"
			logger.error( error_message )
			message_response = self.json_message.createErrorMessage( command, error_message  )

		return message_response

	def handleUserEditPassword(self, messageJson, logger):
		"""
		This function is a password.
		"""
		command = COMMAND_USER_EDIT_PASSWORD

		if "user_info" in messageJson:

			user_info = messageJson["user_info"]
			username = ""

			if "username" in user_info:
				username = user_info["username"]

			# Store the new user in the system.
			user_info_edit_password_confirmed = UserManagement.editUserPassword( user_info )

			if user_info_edit_password_confirmed != None:
				# Success in editing user password.
				logger.info( "Successfully changed the password for %s" % username )
				message_response = self.json_message.createResponseMessage(command)
				message_response["user_info"] = user_info_edit_password_confirmed
			else:
				# Tell the user we couldn't find the user to delete
				logger.info( "Failed to change the password for %s" % username )
				message_response = self.json_message.createErrorMessage( command, "Error: We could not change the user password for %s" % username )

		else:
			message_response = self.json_message.createErrorMessage( command, "Error: We could not find user_info object" )

		return message_response

	def handleUserLogout(self, messageJson, options, logger):
		"""
		This function logs a particular user out.  Only admins should be allowed to call this function.

		TODO: Verify that the current user submitting this request has permissions to perform this action.
		"""

		command = COMMAND_LOGOUT

		# Check if the user passed the token they want to logout in the message.
		if "token" in messageJson:
			username = UserManagement.getUsername( messageJson["token"] )

			if username == None:
				message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, "Could not find the username for this token" )
				return message_response

			# Note that this function logs out the user with the current token, but does not remove all
			#  of that users tokens, only this specific one.
			result = UserManagement.logoutUser( messageJson["token"] )

			if result == True:
				if username != None:
					logger.info( "Logged out user %s, users token removed." % username )

				message_response = self.json_message.createResponseLogoutMessage()
				return message_response
			else:
				logger.info( "Logged out user %s, users token removed." % username )
				message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, "Token found in request but not valid, could not logout" )
				return message_response

			return

		elif "token" in options:

			# If the user didn't specify the token in the message, use it from the options field if it
			# is present
			token = options["token"]

			if token != None:
				username = UserManagement.getUsername( token )

				if username == None:
					message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, "Could not find the username for this token" )
					return message_response

				result = UserManagement.logoutUser( token )

				if result == True:
					if username != None:
						logger.info( "Logged out user %s" % username )

					message_response = self.json_message.createResponseLogoutMessage()
					return message_response
				else:
					message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, "Token found in request by not valid, could not logout" )
					return message_response

				return

			else:
				# We couldn't find the token to logout the user.
				message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, "Token not found, could not logout" )
				return message_response


	def handleUserLogin(self, messageJson, logger):
		"""
		This function handles logging the user in.
		"""

		command = COMMAND_LOGIN

		if "user_login_info" in messageJson:
			user_login_info = messageJson["user_login_info"]

			if "username" in user_login_info:
				username = str(user_login_info["username"])

			if "password" in user_login_info:
				password = str(user_login_info["password"])

		if username == None or password == None:
			reason = "Username or password not provided to log user in"
			message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, reason )
			return message_response

		# TODO: Don't like that reason = token when success, how to make this better?
		result, reason = UserManagement.verifyAndLoginUser( username, password )

		if result == False:
			logger.error( reason )
			message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, reason )
			return message_response

		else:
			token = reason
			logger.info( "Logged in user %s" % username )
			# Now send the token back to the client
			message_response = self.json_message.createResponseLoginMessage( token )
			return message_response

	def handleUserRegister(self, messageJson, logger):
		"""
		Here we are going to register a new user to the system.  After we register them, we log
		them in and send them back a token that they can use to access the system.
		"""

		command = COMMAND_USER_REGISTER

		if "user_info" in messageJson:
			result, reason = UserManagement.addNewUser( messageJson["user_info"] )

			if result == None:
				logger.error( reason )
				message_response = self.json_message.createErrorMessage( "reply", command, reason )
				return message_response
			else:

				username = messageJson["user_info"]["username"]

				# Since we have now created a registered user, we should log them in
				# and give them their token so they can access the site.
				token = UserManagement.loginUser( username )

				logger.info( "Registered and logged in user %s" % username )

				# Now send the token back to the client
				json_response = self.json_message.createResponseRegisterMessage( token )
				return json_response

	def handleStripeCharge(self, messageJson, logger):
		"""
		Handles a Stripe Charge request.
		"""

		command = COMMAND_STRIPE_CHARGE
		STRIPE_TOKEN_KEY = "stripe_token"

		message_response = self.json_message.createResponseMessage( command )

		if STRIPE_TOKEN_KEY in messageJson:
			chargeResult = GravityCharge.stripeCharge( messageJson[STRIPE_TOKEN_KEY] )
			message_response["result"] = chargeResult["status"]
		else:
			reason = "Failed stripe charge because %s is not present in json message" % STRIPE_TOKEN_KEY
			logger.error( reason )
			message_response = self.json_message.createErrorMessage( command, reason )

		return message_response

	def handleStripeGetKeys(self, messageJson, logger):
		"""
		This function returns the keys needed for stripe to function to the user.
		Returns the Stripe public key that is stored in our .env file
		"""

		command = COMMAND_STRIPE_GET_KEYS
		STRIPE_PK_KEY = "STRIPE_PK"

		message_response = self.json_message.createResponseMessage( command )

		try:
			message_response["stripe_pk_key"] = os.getenv("STRIPE_PK")

		except:
			reason = "Failed to return stripe keys because %s is missing from the environment" % STRIPE_PK_KEY
			logger.error( reason )
			message_response = self.json_message.createErrorMessage( command, reason )

		return message_response

	def handleStripeGetSession(self, messageJson, logger):
		"""
		Returns the stripe session information used for Stripe Checkout, which is sent from the javascript on
		the client.

		"""

		command = COMMAND_STRIPE_GET_SESSION

		message_response = self.json_message.createResponseMessage( command )

		if "stripe_sku" in messageJson:
			sku = messageJson["stripe_sku"]

			result = GravityCharge.stripeCheckout(sku)

			message_response["session"] = result

			return message_response

		else:
			message_response = self.json_message.createErrorMessage( MSG_TYPE_REPLY, command, "Could not find strip_sku" )
			return message_response

	def handlePhilTest(self, messageJson, logger):

		message_response = {}

		command = "read_file"
		message_response["command"] = command

		avwatch_obj = open("avwatch.txt", "r")
		text = avwatch_obj.readlines()
		avwatch_obj.close()

		message_response["file"] = text

		return message_response