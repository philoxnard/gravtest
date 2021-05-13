#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

This file allows you to register and create a new contact.

"""

import datetime
import json

# **** Local Import ****
from JsonFile import *
from GravityConfiguration import *

# List Definitions
DEFAULT_GENERAL_LIST_TAG = "general"
DEFAULT_GENERAL_LIST_NAME = "General Contact List"

# Keys
KEY_FIRST_NAME = "first_name"
KEY_LAST_NAME = "last_name"
KEY_EMAIL = "email"
KEY_PHONE = "phone"
KEY_EVENT_NAME = "event_name"
KEY_LIST_NAME_TAG = "list_name_tag"

class GravityContacts():

	def __init__(self):
		pass

	def validateContactInfo(self, contactInfo):
		"""
		Make sure that critical fields are present.  For now that's just the "email"
		tag.
		"""

		if "email" not in contactInfo:
			return False

		return True

	def contactAdd(self, newContactInfo, contactListInfo=None):
		"""
		This function allows us to add a contact to the system.

		contactListInfo contains the information we wish to store from the contact and must match
		what is found in contacts.schema

		TODO: There should be a specific page for each event you go to that allows you to register contacts
		      for each event.
		"""

		if contactListInfo != None and KEY_LIST_NAME_TAG in contactListInfo:
			list_name_tag = contactListInfo[KEY_LIST_NAME_TAG]
		else:
			list_name_tag = DEFAULT_GENERAL_LIST_TAG

		# Find the contact file.
		contacts_file_path = GravityConfiguration.getContactsFile()
		contact_lists = JsonFile.readJsonFile( contacts_file_path )

		if contact_lists == None:
			contact_lists = {}

		# We are going to separate contacts with different keys.  A key could just be "general"
		# or it could be for a specific event.  This way we will know when and how we got the contact.

		new_contact = {}
		new_contact["datetime_created"] = datetime.datetime.now().ctime()

		if KEY_FIRST_NAME in newContactInfo:
			new_contact[KEY_FIRST_NAME] = newContactInfo[KEY_FIRST_NAME]

		if KEY_LAST_NAME in newContactInfo:
			new_contact[KEY_LAST_NAME] = newContactInfo[KEY_LAST_NAME]

		if KEY_EMAIL in newContactInfo:
			new_contact[KEY_EMAIL] = newContactInfo[KEY_EMAIL]

		if KEY_EVENT_NAME in newContactInfo:
			new_contact[KEY_EMAIL] = newContactInfo[KEY_EVENT_NAME]

		if KEY_PHONE in newContactInfo:
			new_contact[KEY_PHONE] = newContactInfo[KEY_PHONE]

		if list_name_tag not in contact_lists:
			contact_lists[list_name_tag] = {}
			contact_lists[list_name_tag]["list"] = []
			contact_lists[list_name_tag]["name"] = DEFAULT_GENERAL_LIST_NAME

		# Before we add this user to the list, we should check to make sure they are not already on the list.
		contact_list = contact_lists[list_name_tag]["list"]

		if contact_list != None:
			for contact in contact_list:
				if "email" in contact and contact[KEY_EMAIL] == newContactInfo[KEY_EMAIL]:
					# This user is already in this list, don't add them again.
					reason = "This user is already in the list."
					return False, reason

		contact_lists[list_name_tag]["list"].append( new_contact )

		result = JsonFile.writeJsonFile( contact_lists, contacts_file_path )

		if result == False:
			reason = "Error: Could not write to contacts file."
			print(reason)
			return None, reason
		else:
			return True, None

	def contactEdit(self, contactInfo, contactListInfo=None):
		"""
		Allows you to edit a contact information
		"""

		if self.validateContactInfo( contactInfo ) == False:
			return False

		# Find the contact file.
		contacts_file_path = GravityConfiguration.getContactsFile()
		contact_lists = JsonFile.readJsonFile( contacts_file_path )

		list_name_tag = DEFAULT_GENERAL_LIST_TAG
		if contactListInfo != None and "list_name_tag" in contactListInfo:
			list_name_tag = contactListInfo["list_name_tag"]

		if list_name_tag not in contact_lists or "list" not in contact_lists[list_name_tag]:
			# TODO: Change this so we just validate the file with the schema so we don't have
			#       to check this here.
			print("Contact list file has incorrect schema")
			return False

		current_list = contact_lists[list_name_tag]["list"]

		for index in range(0, len(current_list)):

			if current_list[index]["email"] == contactInfo["email"]:
				
				if "first_name" in contactInfo:
					current_list[index]["first_name"] = contactInfo["first_name"]

				if "last_name" in contactInfo:
					current_list[index]["last_name"] = contactInfo["last_name"]

				if "phone" in contactInfo:
					current_list[index]["phone"] = contactInfo["phone"]

		result = JsonFile.writeJsonFile( contact_lists, contacts_file_path )

		if result == False:
			reason = "Error: Could not write to contacts file."
			print(reason)
			return None, reason
		else:
			return True, None

	def contactDelete(self, contactInfo, contactListInfo=None):
		"""
		This function deletes a contact from the list.
		"""

		if self.validateContactInfo( contactInfo ) == False:
			return None, "Error: contactInfo passed invalid"

		# Find the contact file.
		contacts_file_path = GravityConfiguration.getContactsFile()
		contact_lists = JsonFile.readJsonFile( contacts_file_path )

		list_name_tag = DEFAULT_GENERAL_LIST_TAG
		if contactListInfo != None and "list_name_tag" in contactListInfo:
			list_name_tag = contactListInfo["list_name_tag"]

		current_list = contact_lists[list_name_tag]["list"]

		for index in range(0, len(current_list)):

			if current_list[index]["email"] == contactInfo["email"]:
				del current_list[index]
				result = JsonFile.writeJsonFile( contact_lists, contacts_file_path )

				if result == False:
					reason = "Error: Could not write to contacts file."
					print(reason)
					return None, reason
				else:
					return True, None

		return None, "Error: Could not find contact to delete"

	def contactsGet(self, listNameTag=None):
		"""
		Gets the Contacts to show
		"""

		# Find the contact file.
		contacts_file_path = GravityConfiguration.getContactsFile()
		contact_lists = JsonFile.readJsonFile( contacts_file_path )

		if contact_lists == None:
			contact_lists = {}

		# TODO: Make this general
		if DEFAULT_GENERAL_LIST_TAG in contact_lists:
			return contact_lists[DEFAULT_GENERAL_LIST_TAG]
		else:
			return None


if __name__ == '__main__':

	contact = {}
	contact[KEY_EMAIL] = "info@creativecollisionstech.com"
	contact[KEY_FIRST_NAME] = "Patrick"
	contact[KEY_LAST_NAME] = "Farrell"
	contact[KEY_PHONE] = "(123) 456 - 7890"

	gravity_contacts = GravityContacts()
	gravity_contacts.contactAdd( contact )