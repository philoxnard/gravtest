#!/usr/bin/env python

"""

GravityEvents.py

This file manages Gravity Events.  This allow

Written by: J. Patrick Farrell
Copyright 2019

TODO: This is very basic right now, need to add event time storage, formatting and many other things.

"""

import datetime
import json
import uuid

# **** Local Import ****
from JsonFile import *
from GravityConfiguration import *

DEFAULT_ALT_IMAGE = "/img/unsplash/jakob-dalbjorn-cuKJre3nyYc-unsplash.jpg"

class GravityEvents():

	def __init__(self):
		pass

	def createEvent(self, eventTitle, eventDateTime, eventLocation, eventDescription, eventImagePath=None):
		"""
		This function creates an event and saves it within a file called events.json
		"""

		events_file_path = GravityConfiguration.getEventsFile()
		current_events = JsonFile.readJsonFile( events_file_path )

		if current_events == None:
			current_events = {}

		event_item = {}
		event_item["datetime_created"] = datetime.datetime.now().ctime()
		event_item["title"] = eventTitle
		event_item["datetime"] = eventDateTime
		event_item["location"] = eventLocation
		event_item["description"] = eventDescription

		if eventImagePath != None:
			event_item["image"] = eventImagePath

		# Create the label that we are going to use for the URL.
		# TODO: We need to make this much more robust.
		label = eventTitle.lower().replace(" ", "-")
		label = label.replace("'", "-")
		label = label.replace(",", "-")
		event_item["label"] = label

		# Create a random ID to idenitfy this event.
		random_id = str(uuid.uuid4()).split("-")[0]
		event_item["id"] = random_id

		if "event_items" not in current_events:
			current_events["event_items"] = []

		current_events["event_items"].append( event_item )

		result = JsonFile.writeJsonFile( current_events, events_file_path )

		if result == False:
			reason = "Error: Could not write blog file"
			print(reason)
			return None, reason

		return result

	def editEvent(self, eventItem):
		"""
		This function takes an event item and edits any fields.  If the event could not be found in the system,
		returns with a warning and a reason that event was not found.
		"""

		events_file_path = GravityConfiguration.getEventsFile()
		gravity_events = JsonFile.readJsonFile( events_file_path )

		if "label" not in eventItem:
			reason = "Error: Could not edit event because we could not find the event label in eventItem request"
			return None, reason

		event_label = eventItem["label"]

		if gravity_events != None and "event_items" in gravity_events:
			events = gravity_events["event_items"]

			for event in events:

				print(event_label)
				if "label" in event and event["label"] == event_label:
					# We found the event, now edit the settings
					if "title" in eventItem:
						event["title"] = eventItem["title"]

					if "location" in eventItem:
						event["location"] = eventItem["location"]

					if "datetime" in eventItem:
						event["datetime"] = eventItem["datetime"]

					if "description" in eventItem:
						event["description"] = eventItem["description"]

					result = JsonFile.writeJsonFile( gravity_events, events_file_path )

					if result == False:
						reason = "Error: Could not write blog file"
						print(reason)
						return None, reason
					else:
						return True, None

		reason = "Error: Could not find and edit event"
		return None, reason

	def deleteEvent(self, eventLabel):
		"""
		This deletes an event. Cannot be un-done.
		"""

		events_file_path = GravityConfiguration.getEventsFile()
		current_events = JsonFile.readJsonFile( events_file_path )

		if current_events == None:
			return None

		if "event_items" not in current_events:
			reason = "Warning: event_items not found in events file."
			print(reason)
			return None

		events = current_events["event_items"]

		index = 0
		for event in events:
			if "label" in event and event["label"] == eventLabel:
				print("Deleting event %s" % event["title"])
				del events[index]
				break

			index = index + 1

		result = JsonFile.writeJsonFile( current_events, events_file_path )

		if result == False:
			reason = "Error: Could not write events file"
			print(reason)
			return None, reason

		return True, None

	def eventRegister(self, eventItem, registrationInfo):
		"""
		This function allows a user to register for an event.
		"""

		# TODO: Right now we only support registering by event ID, we could support event labels too if we wanted
		#       to add code to look up the label from the event ID.
		if "id" not in eventItem:
			reason = "Error: Could not register for event because we could not find the event id in eventItem request"
			return None, reason

		# Get the event object for this event.
		this_event = None
		if "id" in eventItem:
			this_event = self.getEvent( eventItem["id"] )
		else:
			print("Warning! We can't find the event, which is weird because we can't register for an event that doesn't exist.")

		if this_event == None:
			print("Warning! We couldn't open the events file")
			print("This is weird because you can't open the events file without an event existing.")

		# Find the events registration file.
		events_registration_file_path = GravityConfiguration.getEventsRegistrationFile()
		gravity_event_registrations = JsonFile.readJsonFile( events_registration_file_path )

		if gravity_event_registrations == None:
			print("setting blank registrations")
			gravity_event_registrations = {}

		# Get or create the object for the event registrations for this particular event.
		# TODO: We should only allow this to happen if the event actually exists in the database,
		#       Need to look up that the event being requested here is actually an event in the system.
		if "id" in eventItem and eventItem["id"] in gravity_event_registrations:
			event_registrations_item = gravity_event_registrations[eventItem["id"]]
		else:
			event_registrations_item = {}
			gravity_event_registrations[eventItem["id"]] = event_registrations_item

		if "registrations" not in event_registrations_item:
			event_registrations_item["registrations"] = []

			# Include the title so it's easier to read in the JSON file, but warning! This could get out
			# of sync, fix this in the future.
			if this_event != None:
				event_registrations_item["event_title"] = this_event["title"]

		new_registration = {}
		new_registration["datetime_created"] = datetime.datetime.now().ctime()
		new_registration["first_name"] = registrationInfo["first_name"]
		new_registration["last_name"] = registrationInfo["last_name"]
		new_registration["email"] = registrationInfo["email"]

		if "phone" in registrationInfo:
			new_registration["phone"] = registrationInfo["phone"]

		# Before we register this user for the event, we should check to make sure they are not already
		#  registered, and if they are, return a warning that the user is already registered.
		event_registrations = event_registrations_item["registrations"]

		for registration in event_registrations:
			if "email" in registration and registration["email"] == registrationInfo["email"]:
				# This user is already registered, we shouldn't register them again.
				reason = "This user is already registered."
				return False, reason

		event_registrations_item["registrations"].append( new_registration )

		result = JsonFile.writeJsonFile( gravity_event_registrations, events_registration_file_path )

		if result == False:
			reason = "Error: Could not write to event registration file."
			print(reason)
			return None, reason
		else:
			return True, None

	def eventAttendeeCheckIn(self, eventItem, registrationInfo):
		"""
		This function checks in (or out) an attendee into a particular event.

		TOOD: Right now this function just toggles the checkin, we should handle it
		      explicitly.
		"""

		# Find the events registration file.
		events_registration_file_path = GravityConfiguration.getEventsRegistrationFile()
		gravity_event_registrations = JsonFile.readJsonFile( events_registration_file_path )

		if gravity_event_registrations == None:
			reason = "Error: Trying to checkin an attendee, but the attendee file is missing"
			print(reason)
			return None, reason

		if "id" in eventItem and eventItem["id"] in gravity_event_registrations:
			event_registrations_item = gravity_event_registrations[eventItem["id"]]

		# We now need to find the attendee registration info.
		event_registrations = event_registrations_item["registrations"]

		for registration in event_registrations:
			if "email" in registration and registration["email"] == registrationInfo["email"]:

				# Toggle the event checkin if it's present
				# TODO: This should handle it not as a toggle but if checkedin is set to False.
				if "checkedin" not in registration:
					registration["checkedin"] = True
				else:
					del registration["checkedin"]

				# Now that we have set that they are checked in, write the file and return back.
				result = JsonFile.writeJsonFile( gravity_event_registrations, events_registration_file_path )

				if result == False:
					reason = "Error: Could not write to event registration file."
					print(reason)
					return None, reason
				else:
					return True, None

		reason = "Warning: We couldn't find the attendee to checkin"
		return None, reason

	def eventAttendeeDelete(self, eventItem, registrationInfo):
		"""
		This function deletes an event attendee from a particular event.

		"""

		# Find the events registration file.
		events_registration_file_path = GravityConfiguration.getEventsRegistrationFile()
		gravity_event_registrations = JsonFile.readJsonFile( events_registration_file_path )

		if gravity_event_registrations == None:
			reason = "Error: Trying to checkin an attendee, but the attendee file is missing"
			print(reason)
			return None, reason

		if "id" in eventItem and eventItem["id"] in gravity_event_registrations:
			event_registrations_item = gravity_event_registrations[eventItem["id"]]

		# We now need to find the attendee registration info.
		event_registrations = event_registrations_item["registrations"]

		for registration in event_registrations:
			if "email" in registration and registration["email"] == registrationInfo["email"]:

				event_registrations.remove( registration )

				# Now that we have set that they are checked in, write the file and return back.
				result = JsonFile.writeJsonFile( gravity_event_registrations, events_registration_file_path )

				if result == False:
					reason = "Error: Could not write to event registration file."
					print(reason)
					return None, reason
				else:
					return True, None

		reason = "Warning: We couldn't find the attendee to delete from the event registrations"
		return None, reason

	def eventAttendeeEdit(self, eventItem, registrationInfo):
		"""
		This function edits an event attendee from a particular event.

		"""

		# Find the events registration file.
		events_registration_file_path = GravityConfiguration.getEventsRegistrationFile()
		gravity_event_registrations = JsonFile.readJsonFile( events_registration_file_path )

		if gravity_event_registrations == None:
			reason = "Error: Trying to checkin an attendee, but the attendee file is missing"
			print(reason)
			return None, reason

		if "id" in eventItem and eventItem["id"] in gravity_event_registrations:
			event_registrations_item = gravity_event_registrations[eventItem["id"]]

		# We now need to find the attendee registration info.
		event_registrations = event_registrations_item["registrations"]

		for registration in event_registrations:
			if "email" in registration and registration["email"] == registrationInfo["email"]:

				if "email" in registrationInfo:
					registration["email"] = registrationInfo["email"]

				if "first_name" in registrationInfo:
					registration["first_name"] = registrationInfo["first_name"]

				if "last_name" in registrationInfo:
					registration["last_name"] = registrationInfo["last_name"]

				if "phone" in registrationInfo:
					registration["phone"] = registrationInfo["phone"]

				# Now that we have set that they are checked in, write the file and return back.
				result = JsonFile.writeJsonFile( gravity_event_registrations, events_registration_file_path )

				if result == False:
					reason = "Error: Could not write to event registration file."
					print(reason)
					return None, reason
				else:
					return True, None

		reason = "Warning: We couldn't find the attendee to delete from the event registrations"
		return None, reason

	def getEvent(self, eventIdentifier):
		"""
		This gets a particular event based on the event identifier.
		The eventIdentifier can be either the event label or the event ID.
		"""

		events_file_path = GravityConfiguration.getEventsFile()
		gravity_events = JsonFile.readJsonFile( events_file_path )

		if gravity_events != None and "event_items" in gravity_events:
			events = gravity_events["event_items"]

			for event in events:
				# First check if the eventIdentifier matches the event ID
				if "id" in event and event["id"] == eventIdentifier:
					return event

				# If we didn't find it based on the ID, check based on the label.
				if "label" in event and event["label"] == eventIdentifier:
					return event

		return None

	def getEventRegistrationList(self, eventIdentifier):
		"""
		Get the event registration list for a particular event based on the event identifier.
		"""
		event = self.getEvent( eventIdentifier )

		if event == None:
			print("We could not find an event with that identifier")
			return None

		# Find the events registration file.
		events_registration_file_path = GravityConfiguration.getEventsRegistrationFile()
		gravity_event_registrations = JsonFile.readJsonFile( events_registration_file_path )

		if gravity_event_registrations != None:
			if eventIdentifier in gravity_event_registrations and "registrations" in gravity_event_registrations[eventIdentifier]:
				return gravity_event_registrations[eventIdentifier]

		return None

	# **** Getters ****

	def getEventItems(self):

		events_file_path = GravityConfiguration.getEventsFile()
		current_events = JsonFile.readJsonFile( events_file_path )

		if current_events != None and "event_items" in current_events:

			# If there is no image set, set the default event image.
			for event in current_events["event_items"]:
				if "image" not in event:
					event["image"] = DEFAULT_ALT_IMAGE

			return current_events["event_items"]

		return None

if __name__ == '__main__':

	gravity_events = GravityEvents()

	#gravity_events.createEvent( "Test Event", "12/1/2019 10:00 AM", "Washington, DC", "Be inspired by these world changers." )

	"""
	event_item = {}
	event_item["label"] = "Test-event-2"

	registration_info = {}
	registration_info["first_name"] = "Patrick"
	registration_info["last_name"] = "Farrell"
	registration_info["email"] = "patrick@test.com"

	gravity_events.eventRegister( event_item, registration_info )
	"""
	event_registrations = gravity_events.getEventRegistrations( "34ee2cf2" )
	print(json.dumps( event_registrations ))
