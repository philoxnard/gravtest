#!/usr/bin/python

"""
Client code that interacts with the web server over AJAX requests.

Written by: J. Patrick Farrell
Copyright 2018 Creative Collisions Technology, LLC

TODO: Note that you currently have to only use this with http

"""

import requests, json

class GravityAjaxApi():

	def __init__(self):

		self.url = "http://localhost"
		self.token = ""

	def sendMessage(self, message):

		header = {"Content-Type": "application/json"}
		payload = message

		response_decoded_json = requests.post(self.url, data=json.dumps(payload), headers=header)
		response_json = response_decoded_json.json()

		return response_json

	def ajaxTest(self):

		header = {"Content-Type": "application/json"}
		payload = { "command": "ajax_test", "value": "TEST1234" }

		response = self.sendMessage( message )

		print response

	def eventRegister(self, eventId=None):
		"""
		This function allows you to register for an event.
		"""

		message = {}

		message["msg_type"] = "request"
		message["command"] = "event_register"
		message["event_item"] = { "id" : "34ee2cf2" }

		registration_info = {}
		registration_info["first_name"] = "Patrick"
		registration_info["last_name"] = "Farrell"
		registration_info["email"] = "patrick@thegravityframework.com"

		message["registration_info"] = registration_info

		response = self.sendMessage( message )

		print response

	def contactAdd(self):

		message = {}

		message["msg_type"] = "request"
		message["command"] = "contact_add"

		contact_info = {}
		contact_info["first_name"] = "Patrick"
		contact_info["last_name"] = "Farrell"
		contact_info["email"] = "patrick@thegravityframework.com"

		message["contact_info"] = contact_info
		message["token"] = self.token

		#contact_list_info = {}
		#contact_list_info["list_name_tag"] = "test"
		#message["contact_list_info"] = contact_list_info

		response = self.sendMessage( message )

		print response

	def login(self):

		message = {}
		message["command"] = "login"

		user_login_info = {}
		user_login_info["username"] = "pfarrell85@gmail.com"
		user_login_info["password"] = "password"

		message["user_login_info"] = user_login_info

		response = self.sendMessage( message )

		#json_message = json.loads( response )
		json_message = response

		print response

		if "token" in json_message:
			self.token = json_message["token"]
			print("token is %s" % self.token)

if __name__ == "__main__":

	gravity_api = GravityAjaxApi()
	#gravity_api.eventRegister()
	#gravity_api.login()
	gravity_api.contactAdd()