#!/usr/bin/env python

"""
UserManagement.py: Class that manages all of the users in the system.
Copyright 2019 Creative Collisions Technology, LLC

Written by: J. Patrick Farrell
Copyright 2020 Creative Collisions Tech, LLC

This file handles user manangement of the system.

Note that currently all registered users of the system are members, but
not all members have admin or web privileges.

"""

import argparse
import json
from jsonschema import validate

# **** Local Imports ****
from JsonFile import *
from JsonWebToken import *
from GravityConfiguration import *

USER_PERMISSION_ADMIN = "admin"
USER_PERMISSION_WEB = "web"

USE_BLOWFLISH_PASSWORD_HASH = False

if USE_BLOWFLISH_PASSWORD_HASH == True:
	import bcrypt # For password hashing, using OpenBSD's blowfish password hashing
else:
	from passlib.hash import md5_crypt

class UserManagement():
	"""
	TODO: Move this into it's own class.
	"""

	@staticmethod
	def getCredentials():
		"""
		TODO: username and password should not be stored in the config file, they should be stored
				in a separate file or match the linux username and password
		"""

		credentials_file = GravityConfiguration.getUserFilePath()

		json_config = JsonFile.readJsonFile( credentials_file )

		if json_config == None:
			print("Users credentials file (%s) is missing, no users present." % credentials_file)
			credentials = []
		else:
			if "credentials" in json_config:
				credentials = json_config["credentials"]
			else:
				credentials = []

		return credentials

	@staticmethod
	def createUserObject(username, password):
		"""
		This creates a new user object.

		TODO: This is only for debugging right now but should become it's own class to
		      create and validate itself.  Not yet used in production.
		"""

		json_user_object = {}
		json_user_object["username"] = username
		json_user_object["password"] = password
		json_user_object["password_confirm"] = password

		json_user_object["first_name"] = "unknown"
		json_user_object["last_name"] = "unknown"
		json_user_object["permissions"] = {}
		json_user_object["permissions"][USER_PERMISSION_ADMIN] = False
		json_user_object["permissions"][USER_PERMISSION_WEB] = True

		return json_user_object

	@staticmethod
	def validateUserInfo(jsonUserInfo):
		"""
		This function validates that the user info object has all of the required fields we need
		to add add a user.

		TODO: Return more than None, give caller the reason.  Also validate that it matches the schema.
		"""

		if "username" not in jsonUserInfo or jsonUserInfo["username"] == "":
			print("No username")
			return False

		if "first_name" not in jsonUserInfo or jsonUserInfo["first_name"] == "":
			print("No first_name")
			return False

		if "last_name" not in jsonUserInfo or jsonUserInfo["last_name"] == "":
			print("No last_name")
			return False

		if "permissions" not in jsonUserInfo:
			print("No permissions")
			return False

		if "password" not in jsonUserInfo or jsonUserInfo["password"] == "":
			print("No password")
			return False

		if "password_confirm" not in jsonUserInfo or jsonUserInfo["password_confirm"] == "":
			print("No password_confirm")
			return False

		return True

	@staticmethod
	def addNewUser(jsonUserInfo):
		"""
		Handles a request from the client to add a new user to the system.

		TODO: We need to check that jsonUserInfo matches the schema.
		TODO: If a "permissions" object is not present, add a default one.
		"""

		# Before we load in the new user, make sure the user object matches the required schema
		json_schema_object = JsonFile.readJsonFile( USERS_SCHEMA )

		if json_schema_object == None:
			reason = "Error: Could not read JSON schema file (%s)" % USERS_SCHEMA
			print(reason)
			return None, reason

		try:
			validate( json_schema_object, jsonUserInfo )
		except jsonschema.exceptions.ValidationError as ve:
			reason = "Error: JSON object is not valid: %s" % ve
			print(reason)
			return False, reason
		except Exception as e:
			reason = "Error: JSON object is not valid: %s" % e
			print(reason)
			return False, reason

		# TODO: First validate that the format of this JSON object matches the schema.

		# First we should check that the password and password confirm are the same, otherwise we should
		#  reject this request.
		if jsonUserInfo["password"] != jsonUserInfo["password_confirm"]:
			reason = "Error: Passwords do not match, we cannot add user"
			print(reason)
			return None, reason
		else:
			# We want to store hashed passwords, not in plain text.
			hashed_password = UserManagement.generatePasswordHash( str(jsonUserInfo["password"]).strip() )

			# Set the password to be the hashed password.
			jsonUserInfo["password"] = hashed_password

			# We don't want to store the password_confirm in the storage file, so remove it.
			if 'password_confirm' in jsonUserInfo:
				del jsonUserInfo['password_confirm']

		# Next check that there is a "permissions" object and if there isn't one, add a default one
		# TODO: This shouldn't be defaulted to have admin True in the future.
		if "permissions" not in jsonUserInfo:
			jsonUserInfo["permissions"] = { "admin" : True, "web" : True }

		# Second get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		# credentials should be an array of users
		#  First we have to check through the array and make sure that we don't already have a user for this username.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == str(jsonUserInfo["username"]).strip():
				reason = "We already found user %s" % current_user["username"]
				print(reason)
				return None, reason  #TODO: Return object that tells us that the user already exists.

		# We don't want to store the password_confirm in the storage file, so remove it.
		if 'password_confirm' in jsonUserInfo:
			del jsonUserInfo['password_confirm']

		# If we don't have a user with this user name yet, add it to the current_credientials array and write the file.
		current_credentials.append( jsonUserInfo )

		json_object = {}
		json_object["credentials"] = current_credentials

		# This actually writes the new information to the file system.
		result = JsonFile.writeJsonFile( json_object, GravityConfiguration.getUserFilePath() )

		if result == False:
			reason = "Error: Could not write configuration file"
			print(reason)
			return None, reason

		# Now return the new user object back to the calling function, but remove the password
		#  so that is not passed back to the client for security.
		if 'password' in jsonUserInfo:
			del jsonUserInfo['password']

		return True, jsonUserInfo


	@staticmethod
	def updateUserInSubSystems(jsonUserObject):
		"""
		This function handles what happens when a user permissions are updated while the system is
		running.

		TODO: There is some reduncancy between this functions and the functions above, consolidate.
		"""

		if jsonUserObject["permissions"][USER_PERMISSION_WEB] == False:
			print("going to revoke user token for %s" % jsonUserObject["username"])
			# Revoke any Tokens this user may have had.
			UserManagement.revokeUserTokens( jsonUserObject["username"] )

		# TODO: We need to do things here like delete a Samba user if their permissions were revoked,
		#       or add a samba user if that permissions was added.  The problem is we no longer have the plaintext
		#       password to do it, the password is now stored hashed, but to create a Samba user we need it in plaintext.



	@staticmethod
	def deleteUser(jsonUserInfo):
		"""
		Handle a request to delete a user from the system.

		TODO: We need to check that jsonUserInfo matches the schema.  Only username is required to delete a user.
		TODO: We also need to verify that the user requesting to delete a user isn't deleting themselves and they have permission
		        to perform this operation as an admin.
		"""

		# TODO: First check that the user submitting this request has permission to perform this action.

		# Second get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		user_index = 0
		remove_index = -1

		# Loop over the array to find the index of user we need to delete.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == str(jsonUserInfo["username"]).strip():
				remove_index = user_index

			user_index = user_index + 1

		if remove_index != -1:

			json_user_info = current_credentials[remove_index]

			# If we found the user, remove the user from the array, write the user file and return the user
			del current_credentials[ remove_index ]

			#TODO: Probably should have a function that we pass credentials into.
			json_object = {}
			json_object["credentials"] = current_credentials

			# Write the user credentials back to the file system.
			result = JsonFile.writeJsonFile( json_object, GravityConfiguration.getUserFilePath() )

			return jsonUserInfo
		else:
			# We didn't find the user, return None so we can alert the user that we couldn't remove a user that doesn't exist.
			return None

	@staticmethod
	def editUser(jsonUserInfo):
		"""
		Handle a request to edit a user from the system.

		TODO: We need to check that jsonUserInfo matches the schema.  Only username is required to delete a user.
		TODO: We also need to verify that the user requesting to delete a user isn't deleting themselves and they have permission
		        to perform this operation as an admin.
		"""

		# TODO: First check that the user submitting this request has permission to perform this action.

		# Second get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		user_index = 0

		# Loop over the array to find the index of user we need to delete.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == str(jsonUserInfo["username"]).strip():
				break

			user_index = user_index + 1

		# Check if we found the user and update if so.
		if user_index < len(current_credentials):

			# Set any new fields from the user info object that is being passed, leave everything else alone.
			#  Password changes are handled in a separate function.
			if "first_name" in jsonUserInfo:
				current_credentials[user_index]["first_name"] = str(jsonUserInfo["first_name"]).strip()

			if "last_name" in jsonUserInfo:
				current_credentials[user_index]["last_name"] = str(jsonUserInfo["last_name"]).strip()

			if "permissions" in jsonUserInfo:

				if "permissions" not in current_credentials[user_index]:
					current_credentials[user_index]["permissions"] = {}

				edit_permissions = jsonUserInfo["permissions"]

				# TODO: Should check that these fields exist
				if USER_PERMISSION_ADMIN in edit_permissions:
					current_credentials[user_index]["permissions"][USER_PERMISSION_ADMIN] = edit_permissions[USER_PERMISSION_ADMIN]

				if USER_PERMISSION_WEB in edit_permissions:
					current_credentials[user_index]["permissions"][USER_PERMISSION_WEB] = edit_permissions[USER_PERMISSION_WEB]

			#TODO: Probably should have a function that we pass credentials into.
			json_object = {}
			json_object["credentials"] = current_credentials

			# Write the user credentials back to the file system.
			result = JsonFile.writeJsonFile( json_object, GravityConfiguration.getUserFilePath() )

			if result == False:
				print("Error: Could not write users file.")
				return None

			json_user_object = current_credentials[user_index]

			return jsonUserInfo
		else:
			# We didn't find the user, return None so we can alert the user that we couldn't remove a user that doesn't exist.
			return None


	@staticmethod
	def editUserPassword(jsonUserInfo, options=None):
		"""
		TODO: Should the password be stored in a separate file?
		TODO: We need to hash the password and not store it in plain text.

		If an options object is passed with "logout_user" set to True, revoke all the users tokens.
		"""
		# Second get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		user_index = 0

		# Loop over the array to find the index of user we need to delete.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == str(jsonUserInfo["username"]).strip():
				break

			user_index = user_index + 1

		# Check if we found the user and update if so.
		if user_index < len(current_credentials):

			if "password" in jsonUserInfo and "password_confirm" in jsonUserInfo:

				if str(jsonUserInfo["password"]).strip() == str(jsonUserInfo["password_confirm"]).strip():

					# Before we edit and has this users new password, we need to update the password in all of the
					#  sub-systems that have separate users.
					# Since we don't require all of the information to be passed in about the current state of this user
					#  from the client, we need to pass into this function the 
					json_user_info_update = current_credentials[user_index]

					# Set the new password in this object because we need the plain text password for this function
					json_user_info_update["password"] = jsonUserInfo["password"]

					# Before we store the password, hash it so it isn't stored in plain text
					# Hash a password for the first time, with a randomly-generated salt
					hashed_password = UserManagement.generatePasswordHash( str(jsonUserInfo["password"]).strip() )

					# Passwords match, set new password
					current_credentials[user_index]["password"] = hashed_password

					#TODO: Probably should have a function that we pass credentials into.
					json_object = {}
					json_object["credentials"] = current_credentials

					print("writing config file that we saved user password")
					# Write the user credentials back to the file system.
					result = JsonFile.writeJsonFile( json_object, GravityConfiguration.getUserFilePath() )

					if result == False:
						print("Could not save the configuration file")
						return None

					if options != None and "logout_user" in options and options["logout_user"] == True:
						# Now that we have changed the users password, we need to revoke any tokens
						#  we have issued to them and force them to login again if the option is set.
						result = UserManagement.revokeUserTokens( current_user["username"] )

						if result == False:
							print("Warning, could not revoke %s's tokens" % current_user["username"])


					# Delete the password and password_confirm fields so they are not returned to the user
					#  for security, otherwise could have plain text passwords show up in client logs.
					del jsonUserInfo["password"]
					del jsonUserInfo["password_confirm"]

					return jsonUserInfo
				else:
					# Passwords did not match return an error
					return None
			else:
				# password or password_confirm was not present in the jsonUserInfo object, cannot set password
				return None

		else:
			# We didn't find the user, return None so we can alert the user that we couldn't remove a user that doesn't exist.
			return None

	@staticmethod
	def getUserPasswordHash(username):
		"""
		This function looks up and returns the password has for a particular username so we can compare it.
		"""

		current_credentials = UserManagement.getCredentials()

		# Loop over the array to find the user
		for current_user in current_credentials:

			if current_user["username"] == username:
				return str(current_user["password"])

		return None

	@staticmethod
	def getUsername(token):

		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			print("Warning: Could not find any tokens.")
			return False

		if token in issued_tokens:
			return issued_tokens[token]

		# If we couldn't find the users token to get the username, return None
		return None

	@staticmethod
	def verifyAndLoginUser(username, password):

		# If we have come this far, then we should have a username and password to log this client.
		# Verify that they are part of the system and have the correct permissions, then issue them a token.
		hashed = UserManagement.getUserPasswordHash( username )

		# Check that we could find the password hash for this user
		if hashed == None:
			reason = "Could not find user %s" % username
			return False, reason

		# Before we check if their password matches, we need to check if the requested user
		#  has permissions to login over HTTPS
		if UserManagement.isWebUser( username ) == False:
			reason = "User %s tried to login but does not have HTTPS permissions" % username
			return False, reason

		try:
			if UserManagement.verifyPassword( password, hashed ):
				# The user has now passed authentication.  We are going to now
				#  send them a token that they can send us to authenticate future requests.

				token = UserManagement.loginUser( username )
				return True, token

			else:
				print("Password is incorrect for user")
				# TODO: Pass an error message back
				reason = "Password is incorrect for user %s" % username
				return False, reason

		except Exception as e:
			print(e)
			reason = "Login Failed, e = %s" % e
			return False, reason

	@staticmethod
	def loginUser(username):
		"""
		This funtion already assumes the password check has passed.  TODO: Put password check in this function.
		"""

		token = JsonWebToken.encodeClientToken( "1" )

		# Before we send them the token back to them, we should store the token here
		#  so we can keep track of the users we have validated.
		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			# Since we couldn't find a token file, we need to create an object for the tokens.
			# Unless there is a problem with the file system this just means that this is the first
			# token we are storing.
			issued_tokens = {}

		issued_tokens[token] = username

		result = JsonFile.writeJsonFile( issued_tokens, GravityConfiguration.getTokensFilePath() )

		if result == None:
			print("Error could not login user")
			return None

		return token

	@staticmethod
	def logoutUser(token):
		"""
		The purpose of this function is to logout a user, which really is just revoking the token
		they were using for validation.
		"""

		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			print("Warning: Trying to logout the user but the token file was not found.")
			return False

		if token in issued_tokens:
			del issued_tokens[token]

			# To save a write, only write if we actually deleted something
			result = JsonFile.writeJsonFile( issued_tokens, GravityConfiguration.getTokensFilePath() )

			if result == False:
				print("Error saving token file")
				return False
			else:
				return True

		# Return False, we didn't actually remove a token
		return False


	@staticmethod
	def revokeUserTokens(username):
		"""
		This function revokes all tokens for a user.

		Note we must check for multiple tokens for a user because if they login from two or more different
		devices, one user could have multiple tokens.
		"""

		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			print("Warning: We are trying to revoke a token, but we couldn't read the token file")
			return False

		tokens_to_remove = []

		# First go through and find all the tokens we should revoke.  Because it is a dictionary
		#  we don't want to do this in one step.
		for token in issued_tokens:
			if issued_tokens[token] == username:
				tokens_to_remove.append( token )

		# Now that we have a list of tokens to revoke, revoke them.
		for token in tokens_to_remove:
			del issued_tokens[ token ]

		# Now write the token file back to disk.
		# TODO: In the future we should add a lock around this file so two threads don't
		#       access it at the same time.
		result = JsonFile.writeJsonFile( issued_tokens, GravityConfiguration.getTokensFilePath() )

		if result == False:
			print("Error saving token file")
			return False
		else:
			return True

	@staticmethod
	def tokenMaintenance():
		"""
		The purpose of this function is to run through all the tokens in the token file and cleanup any
		tokens that have expired or tokens that are issues to users that are no longer valid.
		"""

		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			print("Warning: We are trying run token maintenance, but we couldn't read the token file")
			return False

		tokens_to_remove = []

		# First go through and find all the tokens we should revoke.  Because it is a dictionary
		#  we don't want to do this in one step.
		for token in issued_tokens:

			try:
				jwt = jwt.decode(
					token,
					str("secret")
				)
				print(jwt)
			except jwt.InvalidTokenError:
				return False

	@staticmethod
	def isAdmin(username=None):
		"""
		Checks if this user has administrator privileges
		"""

		if username == None:
			# If no user was passed in, they can't be an admin :)
			return False

		# Get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		# Loop over the array to find the index of user we need to delete.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == username.strip():

				if "permissions" in current_user and current_user["permissions"][USER_PERMISSION_ADMIN] == True:
					return True
				else:
					return False

		return False

	@staticmethod
	def isMember(username=None):
		"""
		Checks if this user has member privileges
		"""

		if username == None:
			# If no user was passed in, they can't be an admin :)
			return False

		# Get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		# Loop over the array to find the index of user we need to delete.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == username.strip():
				# We found the user, it's a member of the system.
				return True


		return False

	@staticmethod
	def isWebUser(username):
		"""
		Checks if this user has web privileges
		"""

		# Get the JSON object of the users that are currently stored in the system.
		current_credentials = UserManagement.getCredentials()

		# Loop over the array to find the index of user we need to delete.
		for current_user in current_credentials:

			if str(current_user["username"]).strip() == username.strip():

				if "permissions" not in current_user:
					# If permissions object not present, assume defaults with HTTP enabled.
					return True
				elif USER_PERMISSION_WEB in current_user["permissions"] and current_user["permissions"][USER_PERMISSION_WEB] == True:
					return True
				else:
					return False

		return False

	@staticmethod
	def generatePasswordHash(password):

		if USE_BLOWFLISH_PASSWORD_HASH:
			return bcrypt.hashpw(str( password ).strip(), bcrypt.gensalt())
		else:
			# Use MD5 for password hashing
			# TODO: Add a salt?
			hashed = md5_crypt.using(salt_size=4).hash( password )

			return md5_crypt.using(salt_size=4).hash( password )

	@staticmethod
	def verifyPassword(plaintextPassword, hashedPassword):

		if USE_BLOWFLISH_PASSWORD_HASH:
			return bcrypt.hashpw(plaintextPassword, hashedPassword) == hashedPassword
		else:
			return md5_crypt.verify(plaintextPassword, hashedPassword)

	@staticmethod
	def validateToken(token):
		"""
		The purpose of this function is to check if the token received by the client
		is in our list of tokens that we are currently holding for validated clients.
		"""
		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			return False

		# Now we are going to check if the token the client just sent is one of our issued tokens.
		if token in issued_tokens:
			# TODO: We should actually decode the token here and check that it is valid and hasn't expired.
			return True

		return False

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--username', '-u', type=str)
	parser.add_argument('--password', '-p', type=str)

	args = parser.parse_args()

	if args.username != None and args.password:

		json_user_object = UserManagement.createUserObject( args.username, args.password )

		UserManagement.addNewUser( json_user_object )
