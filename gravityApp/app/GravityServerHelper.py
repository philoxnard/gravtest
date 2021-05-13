#!/usr/bin/env python

'''
**********************************************************
Gravity Server Helper

This is a helper class that you can use in the event that
you need to run Gravity as a separate thread within a bigger application.

This should be used to create a thread from a main program.

Note: Currently is only setup for HTTP.

Written by: J. Patrick Farrell
Copyright (c) 2021

**********************************************************
'''

import threading

# **** Local Imports ****
from GravityConfiguration import *
from GravityServer import *
from HTTPWebHandler import *

class GravityServerHelper():
	"""
	This is the class that we use to launch the Gravity Web Server
	from a Main application.  This class allows the web
	server to run it it's own separate thread inside of a parent program.
	This is useful if your application requires multiple threaded applications
	running in parallel and communicating with each other.
	"""

	def __init__(self, message_queue=None, sharedVariable=None):

		self.server_stop = False
		self.mts_webserver = None
		self.message_queue = message_queue
		#JsonMessage.setMessageQueueReference(message_queue)

		self.main_thread_status = sharedVariable

	def setMainThreadReference(self, mainStatus):
		self.main_thread_status = mainStatus

	def startThread(self):
		self.startServerThread()

	def startServerThread(self):

		self.thread = threading.Thread(target=self.serverThread, args=(self.main_thread_status, ))
		self.thread.start()

	def serverThread(self, mainThreadStatus):

		server_address = ('', DEFAULT_PORT)

		self.gravity_webserver = GravityHTTPWebServer(server_address, WEBSERVER_ROOT_DIRECTORY, False)

		# Make sure you call this to set the main thread status before you call run.
		if mainThreadStatus != None:
			self.gravity_webserver.setMainThreadReference( mainThreadStatus )

		# If we have a message queue to send messages back up to the main thread, set the reference here.
		if self.message_queue != None:
			self.gravity_webserver.setMessageQueue( self.message_queue )

		self.gravity_webserver.run( HTTPWebHandler )

	def stopThread(self):
		print "GravityServerHelper (stopThread): Stopping Web/API Server"
		self.gravity_webserver.stop()