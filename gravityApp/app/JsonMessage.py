#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019

JsonMessage.py

JSON message parser and message creating functions for the Gravity Server.

"""

import platform
import json

# **** Local Imports ****
from GravityBlog import *
from JsonFile import *   # We are using this to read JSON files, should rename and separate the class.
from JsonMessageCommands import *
from MessageHandlers import *

class JsonMessage():

	@staticmethod
	def createStatusMessage(status):
		"""
		TODO: This doesn't really make sense the way this is defined.  Change status to be a string rather than enum in schema.
		"""

		message = {}
		message["msg_type"] = "status"
		message["status"] = "info"
		message["info"] = status

		return message

	@staticmethod
	def createErrorMessage(msgType, command, reason):

		if command == None:
			return None

		message = {}
		message["msg_type"] = msgType
		message["command"] = command
		message["status"] = "error"
		message["error"] = { "reason" : reason }

		return message

	@staticmethod
	def createWarningMessage(msgType, command, reason):

		if command == None:
			return None

		message = {}
		message["msg_type"] = msgType
		message["command"] = command
		message["status"] = "warning"
		message["warning"] = { "reason" : reason }

		return message

	@staticmethod
	def createResponseMessage(command):

		if command == None:
			return None

		message = {}
		message["msg_type"] = "reply"
		message["command"] = command

		return message

	@staticmethod
	def createResponseLoginMessage(token):
		"""
		This is the response to a login request that contains the token the client can use for authentication.
		"""

		if token == None:
			print("Error: No Token, cannot create message")
			return None

		message = {}
		message["msg_type"] = "reply"
		message["command"] = "login"
		message["token"] = token

		return message

	@staticmethod
	def createResponseLogoutMessage(userInfo=None):
		"""
		This is the base response message which always includes the date and time of the response.
		You must pass in the name of the command that you are returning.
		"""

		message = {}
		message["msg_type"] = "reply"
		message["command"] = "logout"

		if userInfo != None:
			message["user_info"] = userInfo

		return message

	@staticmethod
	def createResponseRegisterMessage(token):
		"""
		This is the response to a login request that contains the token the client can use for authentication.
		"""

		if token == None:
			print("Error: No Token, cannot create message")
			return None

		message = {}
		message["msg_type"] = "reply"
		message["command"] = "register"
		message["token"] = token

		return message


