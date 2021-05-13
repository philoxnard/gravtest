#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

GravityServer.py

MIT License

This is the main entry point into the Gravity Web Server.  This starts
both the HTTP and the HTTPS server.

"""

import argparse
import base64
import json
import os
import signal
import socket # For checking IP Addresses
import sys
import ssl
import platform
import threading
import time
import Queue
import struct
import urllib
import ssl     # For HTTPS

from hashlib import sha1
import errno, socket #for socket exceptions

from SimpleHTTPServer import SimpleHTTPRequestHandler
from BaseHTTPServer import HTTPServer
from base64 import b64encode
from SocketServer import ThreadingMixIn  # To add multi-threading to HTTP Server

# **** Local includes ****
from FileTools import *
from HTTPWebHandler import *
from HTTPRedirectHandler import *
from GravityConfiguration import *
from UserManagement import *
from JsonMessage import *
from LogHelper import *


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

# Serves both http and websockets
class GravityHTTPSWebServer():

	def __init__(self, server_address, directory):

		self.logger = LogHelper(self.__class__.__name__, self.__class__.__name__ + ".log")
		self.logger.setLoggingLevel(INFO_LEVEL)

		if LOG_REQUEST_MESSAGES == True or LOG_RESPONSE_MESSAGES == True:
			"""
			Request and reply messages are tagged as debug, so if we want to see
			them we have to change the logging level to debug
			"""
			self.logger.setLoggingLevel(DEBUG_LEVEL)

		self.logger.printLoggingFile()

		current_mode = GravityConfiguration.getCurrentMode()
		self.logger.info("Starting Server in %s mode" % current_mode)

		self.httpd = None
		self.stop_server = False
		self.server_address = server_address
		self.directory = directory

		# Get the credentials required to login to the server.
		self.credentials = GravityConfiguration.getCredentials()

	def signalHandler(self, signal, frame):
		self.logger.info("You pressed Ctrl+C!, Shutting down server")
		sys.exit()

	def run(self, HandlerClass=HTTPWebHandler, ServerClass=ThreadedHTTPServer):

		ServerClass.daemon_threads = True

		# Set the base path of the directory to find the HTML files.
		HandlerClass.base_path = self.directory
		self.logger.info( "Serving HTML files from the directory %s" % self.directory )

		# Set the Logger
		# Note: By setting this logger here, it's also available in the base class, HTTPWebHandler
		HandlerClass.logger = self.logger

		self.httpd = ServerClass(self.server_address, HandlerClass)

		# Note: This is not handled the best, but we need to have the protocol inside of the class for links.
		#       so since here we are using SSL, we need to set the protocol variable to "https".  Would be nice
		#       if we could get this variable some other way.
		HandlerClass.protocol = "https"

		sa = self.httpd.socket.getsockname()
		#self.httpd.socket.settimeout(1)
		self.logger.info("Serving HTTPS on %s:%s" % (sa[0], sa[1]))
		self.logger.info( "Serving HTML files from directory %s" % self.directory )

		try:
			# Wrap the socket for HTTPS
			self.logger.info( "Wrapping HTTPS socket with certificate (%s)" % PEM_FILE )
			self.httpd.socket = ssl.wrap_socket(self.httpd.socket, certfile=PEM_FILE, server_side=True)
		except IOError as e:
			self.logger.error( "Error: Could not create httpd, exiting (%s)" % e )
			sys.exit(1)

		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			pass
		except:
			pass
		finally:
			# Clean-up server (close socket, etc.)
			self.logger.info( "Closing the HTTPS server" )
			self.httpd.server_close()

	def stop(self):
		try:
			self.httpd.socket.close()
		except:
			self.logger.error( "Inside HTTPS stop, could not close socket" )

# Serves both http and websockets
class GravityHTTPWebServer():

	def __init__(self, server_address, directory, secure=True):

		self.logger = LogHelper(self.__class__.__name__, self.__class__.__name__ + ".log")
		self.logger.setLoggingLevel(INFO_LEVEL)

		if LOG_REQUEST_MESSAGES == True or LOG_RESPONSE_MESSAGES == True:
			"""
			Request and reply messages are tagged as debug, so if we want to see
			them we have to change the logging level to debug
			"""
			self.logger.setLoggingLevel(DEBUG_LEVEL)

		self.logger.printLoggingFile()

		current_mode = GravityConfiguration.getCurrentMode()
		self.logger.info("Starting Server in %s mode" % current_mode)

		self.httpd = None
		self.stop_server = False
		self.server_address = server_address
		self.directory = directory
		self.secure = secure

		# Get the credentials required to login to the server.
		self.credentials = GravityConfiguration.getCredentials()

		# Variables used for multi-threaded applications where Gravity is running in sub-thread.
		self.main_thread_status = None
		self.message_queue = None      # If used, this allows us to send messages to the main thread.


	def signalHandler(self, signal, frame):
		self.logger.info("You pressed Ctrl+C!, Shutting down server")

	def run(self, HandlerClass=HTTPRedirectHandler, ServerClass=ThreadedHTTPServer):

		ServerClass.daemon_threads = True

		# Until I find a better way, store whether we are running in secure or plaintext for redirects
		ServerClass.secure = self.secure

		# Set the base path of the directory to find the HTML files.
		HandlerClass.base_path = self.directory

		# Set the Logger
		# Note: By setting this logger here, it's also available in the base class, HTTPWebHandler
		HandlerClass.logger = self.logger

		self.HandlerClass = HandlerClass

		# Variable used when we need information from a main thread. 'None' if not used.
		self.HandlerClass.main_thread_status = self.main_thread_status

		# Message queue variable to pass messages to the main thread. 'None' if not used.
		self.HandlerClass.message_queue = self.message_queue

		self.httpd = ServerClass(self.server_address, self.HandlerClass)

		sa = self.httpd.socket.getsockname()
		#self.httpd.socket.settimeout(1)
		self.logger.info("Gravity Server Started. Visit %s:%s to view your application" % (sa[0], sa[1]))
		self.logger.info( "Serving HTML files from directory %s" % self.directory )

		GravityConfiguration.setCurrentHostIP( sa[0] )

		try:
			self.httpd.serve_forever()
		except KeyboardInterrupt:
			pass
		except:
			pass
		finally:
			# Clean-up server (close socket, etc.)
			self.logger.info( "Closing the HTTPS server" )
			self.httpd.server_close()

	def setMainThreadReference(self, mainThreadStatus):
		"""
		If you are going to use this, make sure you call this function before you call run.
		"""
		self.main_thread_status = mainThreadStatus

	def setMessageQueue(self, messageQueue=None):
		"""
		This is a message queue that we can used to send messages to the main thread. If Gravity
		is running as the main thread, then this isn't used, but if you have launched Gravity from GravityMain
		and it's running in a sub-thread, then you might want to use this to send messages to the main thread.

		Important: Be sure that you call this function to the set the reference before you call run.
		"""
		self.message_queue = messageQueue

	def stop(self):
		try:
			self.httpd.socket.close()
		except:
			self.logger.info( "Inside HTTP stop, could not close socket" )

class GravityApp():
	"""
	This is the main entry point class for the TM-1 Web Server.  This main application
	class starts up two server threads, one for the HTTP server and one for the HTTPS server.
	"""

	def __init__(self, config):

		GravityConfiguration.dumpEnvironment()

		self.logger = LogHelper(self.__class__.__name__, self.__class__.__name__ + ".log")
		self.START_HTTP_THREAD = True
		self.START_HTTPS_THREAD = True

		self.running = True
		self.secure = config["secure"]        # Set to False if HTTPS is not required.
		self.directory = config["directory"]

		self.logger.info( "Starting Gravity Application" )

		# Generate any sub-configuration files we need.  TM-1's configuration file holds the master
		#  config, but some of the sub-systems need their own configurations.
		"""
		self.logger.info( "Generating Samba Configuration file and configuring shares in sub-system." )
		result = GravitySamba.configureSambaShares()
		if result == None:
			self.logger.error( "Failed to configure Samba sub-system (%s)" % SECURE_APP_SAMBA_CONFIG_FILE )
		"""

		if "HOST_INPUT_DIRECTORY" in config:
			self.logger.info("Setting HOST_INPUT_DIRECTORY = %s" % config["HOST_INPUT_DIRECTORY"] )
			GravityConfiguration.setHostInputDirectory( config["HOST_INPUT_DIRECTORY"] )

		if "HOST_OUTPUT_DIRECTORY" in config:
			self.logger.info("Setting HOST_OUTPUT_DIRECTORY = %s" % config["HOST_OUTPUT_DIRECTORY"] )
			GravityConfiguration.setHostOutputDirectory( config["HOST_OUTPUT_DIRECTORY"] )

		if "HOST_ARCHIVE_DIRECTORY" in config:
			pass
			#self.logger.debug("Setting HOST_ARCHIVE_DIRECTORY = %s" % config["HOST_ARCHIVE_DIRECTORY"] )
			#GravityConfiguration.setHostOutputDirectory( config["HOST_ARCHIVE_DIRECTORY"] )

		# Start threads to do asynchronous I/O
		if self.START_HTTP_THREAD == True:

			server_address = ('', config["http_port"])

			self.logger.info( "Starting Gravity HTTP Server Thread" )
			self.GravityHTTPWebServer = GravityHTTPWebServer( server_address, self.directory, self.secure )

			# Set the signal hander for when the user kills the program
			signal.signal(signal.SIGINT, self.signalHandler)

			self.httpThread = threading.Thread(target=self.GravityHTTPWebServerThread)
			self.httpThread.start()

		# Start threads to do asynchronous I/O
		if self.START_HTTPS_THREAD == True and self.secure == True:

			server_address = ('', config["ssl_port"])

			self.logger.info( "Starting Gravity HTTPS Server Thread" )
			self.GravityHTTPSWebServer = GravityHTTPSWebServer( server_address, self.directory )

			# Set the signal hander for when the user kills the program
			signal.signal(signal.SIGINT, self.signalHandler)

			self.httpsThread = threading.Thread(target=self.GravityHTTPSWebServerThread)
			self.httpsThread.start()

	def GravityHTTPWebServerThread(self):
		"""
		This actually runs the application.

		The default behavior is that we run two server threads.  One with SSL and one without.
		If we have the SSL server thread disabled, we want this HTTP server to actually serve
		web pages rather than just re-direct to HTTPS, so send in the handler that is normally used
		for SSL.  The default handler for HTTP just re-directs to HTTPS.
		"""
		if self.secure == False:
			self.GravityHTTPWebServer.run( HTTPWebHandler )
		else:
			self.GravityHTTPWebServer.run()

	def GravityHTTPSWebServerThread(self):
		"""
		This actually runs the application.
		"""
		self.GravityHTTPSWebServer.run()

	def endApplication(self):

		if self.START_HTTP_THREAD:
			self.logger.info( "Stopping HTTP Server" )
			self.GravityHTTPWebServer.stop()

		if self.START_HTTPS_THREAD and self.secure == True:
			self.logger.info( "Stopping HTTPS Server" )
			self.GravityHTTPSWebServer.stop()

		self.logger.info( "Shutting down Gravity Application" )
		self.running = False
		sys.exit()

	def signalHandler(self, signal, frame):
		print("You pressed Ctrl+C!")
		self.endApplication()

	def run(self):

		while self.running == True:
			time.sleep(1)

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--dir', '-d', default=WEBSERVER_ROOT_DIRECTORY, type=str)
	parser.add_argument('--disable', '-D', action='store_false', default=True)
	parser.add_argument('--http', '-H', default=DEFAULT_PORT, type=int)
	parser.add_argument('--ssl', '-s', default=DEFAULT_SSL_PORT, type=int)
	args = parser.parse_args()

	config = {}
	config["directory"] = args.dir
	config["secure"] = args.disable
	config["http_port"] = args.http
	config["ssl_port"] = args.ssl

	# Check if there were environmental variables passed in and add them to the GravityApp config object.
	try:
		config["HOST_INPUT_DIRECTORY"] = os.environ["HOST_INPUT_DIRECTORY"]
	except:
		pass

	try:
		config["HOST_OUTPUT_DIRECTORY"] = os.environ["HOST_OUTPUT_DIRECTORY"]
	except:
		pass

	try:
		config["HOST_ARCHIVE_DIRECTORY"] = os.environ["HOST_ARCHIVE_DIRECTORY"]
	except:
		pass

	# TODO: "disable" here means we want to disable the SSL server.  Find a better name.
	GravityApp = GravityApp( config )
	signal.signal(signal.SIGINT, GravityApp.signalHandler)
	GravityApp.run()
