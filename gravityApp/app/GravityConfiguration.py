#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019

"""

import datetime
import json

# **** Local Imports ****
from JsonFile import *

LOG_REQUEST_MESSAGES = True
LOG_RESPONSE_MESSAGES = True

TEXT_DATA_OPCODE = 1
BINARY_DATA_OPCODE = 2

# **** Web Server Configuration ****
DEFAULT_PORT = 80
DEFAULT_SSL_PORT = 443

PRINT_API_REQUEST_MESSAGES = False
PRINT_API_RESPONSE_MESSAGES = False

USE_DOCKER = False    # Set this to False when you want to run without Docker

if USE_DOCKER == True:
	# This would be relative to inside of the docker container
	ROOT_DIRECTORY = "/gravity"
	AUTH_DIRECTORY = ROOT_DIRECTORY + "/auth"
	DATA_DIRECTORY = ROOT_DIRECTORY + "/data"
	BLOG_DIRECTORY = DATA_DIRECTORY + "/blog"
	MODELS_ROOT_DIRECTORY = ROOT_DIRECTORY+ "/models"
	VIEWS_ROOT_DIRECTORY = ROOT_DIRECTORY + "/views"
	WEBSERVER_ROOT_DIRECTORY = ROOT_DIRECTORY + "/public" # Directory where we serve our HTML
	SECURITY_FOLDER = ROOT_DIRECTORY + "/security"
	SCHEMA_DIRECTORY = ROOT_DIRECTORY + "/schema"
else:
	ROOT_DIRECTORY = "../.."
	AUTH_DIRECTORY = ROOT_DIRECTORY + "/auth"
	DATA_DIRECTORY = ROOT_DIRECTORY + "/data"
	BLOG_DIRECTORY = DATA_DIRECTORY + "/blog"
	MODELS_ROOT_DIRECTORY = ROOT_DIRECTORY + "/models"
	VIEWS_ROOT_DIRECTORY = ROOT_DIRECTORY + "/views"
	WEBSERVER_ROOT_DIRECTORY = ROOT_DIRECTORY + "/public"
	SECURITY_FOLDER = ROOT_DIRECTORY + "/security"
	SCHEMA_DIRECTORY = ROOT_DIRECTORY + "/schema"

UPLOAD_FOLDER = WEBSERVER_ROOT_DIRECTORY + "/upload"
EVENTS_DATA_DIRECTORY = DATA_DIRECTORY + "/events"

MESSAGE_SCHEMA = SCHEMA_DIRECTORY + "/message.schema"
USERS_SCHEMA = SCHEMA_DIRECTORY + "/users.schema"

PEM_FILE = SECURITY_FOLDER + "/server.pem"

BLOG_FILE_JSON = BLOG_DIRECTORY + "/blog.json"
CONTACTS_FILE_JSON = DATA_DIRECTORY + "/contacts.json"
EVENTS_FILE_JSON = DATA_DIRECTORY + "/events.json"
BLOGS_FILE_JSON = DATA_DIRECTORY + "/blogs.json"
STRIPE_SKU_PRODUCTS = DATA_DIRECTORY + "/products.json"
EVENTS_REGISTRATION_FILE_JSON = EVENTS_DATA_DIRECTORY + "/registrations.json"
USER_FILE_JSON = AUTH_DIRECTORY + "/users.json"
TOKEN_FILE_JSON = AUTH_DIRECTORY + "/tokens.json"

class GravityConfiguration():

	@staticmethod
	def dumpEnvironment():
		"""
		Print current file locations (for debugging)
		"""
		print("CURRENT ENVIRONMENT:")
		print("    USE_DOCKER: %s" % USE_DOCKER)
		print("    USER_FILE_JSON: %s" % USER_FILE_JSON)
		print("    TOKEN_FILE_JSON: %s" % TOKEN_FILE_JSON)
		print("    DEFAULT_PORT: %d" % DEFAULT_PORT)
		print("    DEFAULT_SSL_PORT: %s" % DEFAULT_SSL_PORT)
		print("    SECURITY_FOLDER: %s" % SECURITY_FOLDER)
		print("    VIEWS_ROOT_DIRECTORY: %s" % VIEWS_ROOT_DIRECTORY)
		print("    WEBSERVER_ROOT_DIRECTORY: %s" % WEBSERVER_ROOT_DIRECTORY)

	@staticmethod
	def getContactsFile():
		return CONTACTS_FILE_JSON


	@staticmethod
	def getCurrentMode():
		"""
		This function returns a string we can display to tell the user what
		mode we are currently running in.
		"""

		if USE_DOCKER == True:
			return "Docker Mode"
		else:
			return "Development"

	@staticmethod
	def getCredentials():
		"""
		TODO: username and password should not be stored in the config file, they should be stored
				in a separate file or match the linux username and password
		"""

		credentials_file = USER_FILE_JSON

		json_config = JsonFile.readJsonFile( credentials_file )

		if json_config == None:
			print("Warning, failed to read user credentials file (%s)" % credentials_file)
			return None

		if "credentials" in json_config:
			credentials = json_config["credentials"]
			return credentials

		# Couldn't find the user credentials object
		return None

	@staticmethod
	def getBlogFile():
		return BLOG_FILE_JSON

	@staticmethod
	def getBlogsFile():
		return BLOGS_FILE_JSON

	@staticmethod
	def getEventsFile():
		return EVENTS_FILE_JSON

	@staticmethod
	def getEventsRegistrationFile():
		return EVENTS_REGISTRATION_FILE_JSON

	@staticmethod
	def getPemFilePath():
		return PEM_FILE

	@staticmethod
	def getUploadFolderPath():
		return UPLOAD_FOLDER

	@staticmethod
	def getUserFilePath():
		return USER_FILE_JSON

	@staticmethod
	def getTokensFilePath():
		return TOKEN_FILE_JSON

	@staticmethod
	def getWebDirectory():
		return WEBSERVER_ROOT_DIRECTORY

	# ***** Setters *****

	@staticmethod
	def setHostInputDirectory(inputDirectory):
		"""
		This function is used when there is an environmental variable passed in that specifies the
		location of the host input directory.

		We need this because in the event that we need to call another docker image
		with the path, we can't give it the path inside of this image, we have to give it the path
		to the directory on the host
		"""

		global HOST_INPUT_DIRECTORY
		HOST_INPUT_DIRECTORY = os.path.abspath( inputDirectory )

	@staticmethod
	def setHostOutputDirectory(outputDirectory):

		global HOST_OUTPUT_DIRECTORY
		HOST_OUTPUT_DIRECTORY = os.path.abspath( outputDirectory )

	@staticmethod
	def setCurrentHostIP(hostIp):

		global CURRENT_HOST_IP
		CURRENT_HOST_IP = hostIp
