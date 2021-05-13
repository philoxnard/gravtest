#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

This is a helper class that allows us to validate JSON message based
on a JSON schema file.

"""

import json
import jsonschema
from jsonschema import validate
import sys
import unittest

# **** Local Imports ****
from GravityConfiguration import *
from JsonMessage import *
from JsonFile import *

class JsonSchemaHelper():

	@staticmethod
	def validateMessageSchema(jsonMessageObject):

		json_schema_object = JsonFile.readJsonFile( MESSAGE_SCHEMA )
		#print json.dumps( jsonMessageObject )
		#print json.dumps( json_schema_object )

		if json_schema_object == None:
			print("Error: Could not read JSON schema file (%s)" % MESSAGE_SCHEMA)
			return None

		try:
			validate( jsonMessageObject, json_schema_object )
			return True
		except jsonschema.exceptions.ValidationError as ve:
			print("Error: JSON object is not valid: %s" % ve)
			return False

if __name__ == "__main__":
	"""
	This main is just used for testing.
	"""

	message = payload = { "command": "ajax_test", "value": "TEST1234" }

	print("message = %s" % json.dumps( message ))

	is_valid = JsonSchemaHelper.validateMessageSchema( message )

	if is_valid == True:
		print("Message is valid and matches schema")
	else:
		print("Message is NOT valid, fails schema match")