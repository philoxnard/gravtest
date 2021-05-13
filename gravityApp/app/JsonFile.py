#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

"""

import json
import os

PRETTY_PRINT = True

class JsonFile():

	@staticmethod
	def readJsonFile(jsonFilePath):
		"""
		Reads a JSON file and returns as a JSON object, or None if it can't read
		the JSON file.
		"""

		try:
			json_file = open( jsonFilePath, "r" )

			if json_file == None:
				print("Could not read file %s" % jsonFilePath)
				return None

			json_config_str = json_file.read()

			json_object = json.loads(json_config_str)

			json_file.close()

			if json_object != None:
				return json_object
			else:
				print("Could read from JSON file into JSON object: %s" % jsonFilePath)
				return None
		except IOError:
			print("IOError: Could not read JSON file: %s" % jsonFilePath)
			return None
		except Exception as e:
			reason = "Error: Could not read JSON file: %s" % e
			return None


	@staticmethod
	def writeJsonFile(jsonObject, jsonFilePath=None):
		"""
		TODO: Need to edit this because we are now going to need to store more than just the credentials.
		"""

		if jsonFilePath == None:
			return False

		base_folder, file_name = os.path.split(jsonFilePath)

		if not os.path.exists(base_folder):
			try:
				os.makedirs( base_folder )
			except OSError:
				if not os.path.isdir( base_folder ):
					# We couldn't create the folder where we want to place this file. Else the folder already exists
					return False

		try:
			json_file = open( jsonFilePath, "w" )

			try:
				if PRETTY_PRINT == True:
					json_info_str = json.dumps(jsonObject, indent=4, sort_keys=True)
				else:
					json_info_str = json.dumps(jsonObject)

				json_file.write(json_info_str)
			except:
				print("writeConfigFile: json is not valid, cannot write file")
				json_file.close()
				return False			

			json_file.close()

		except:
			print("Error could not configuration file")
			return False

		return True
