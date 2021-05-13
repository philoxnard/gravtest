#!/usr/bin/env python

'''
**********************************************************
GravityMain.py

Written by: J. Patrick Farrell
Copyright 2021 Creative Collisions Technology, LLC

Main Entry point into the Gravity program.

This lauches the GravityServer in a sub-thread using the
GravityServerHelper class. You can use this main
program to then start other threads that should run in parallel.

If you want to build a separate sub-system, copy the GravityServerHelper
class and have it launch your own class. Then put the hooks from the helper
into runProgram to start the thread for that program.

Make sure you also include the stopThread function so that this
main program closes the other threads properly.


**********************************************************
'''

import signal
import sys
import time
import Queue

# **** Local Imports ****
from GravityServerHelper import *

class GravityMain():

	def __init__(self):

		self.stop_program = False
		self.poll_interval = 1 # second

		# Create the queue to send messages back to MTS
		self.message_queue = Queue.Queue()

		self.gravity_server_helper = GravityServerHelper( self.message_queue )

	def runProgram(self):
		"""
		This is the main entry point into the program. By default it runs the gravity
		server. If you wished to have additional threads running, this is where you would
		start them.
		"""

		# Start the thread for the Gravity Server
		self.gravity_server_helper.startThread()

		while self.stop_program == False:
			time.sleep( self.poll_interval )

	def stopAllThread(self):
		"""
		Stops any thread that are running.
		"""
		self.gravity_server_helper.stopThread()

	def signalHandler(self, signal, frame):
		print('You pressed Ctrl+C! Stopping all the sub-threads.')
		self.gravity_server_helper.stopThread()
		sys.exit()

if __name__ == '__main__':

	gravity_main = GravityMain()

	signal.signal(signal.SIGINT, gravity_main.signalHandler)

	gravity_main.runProgram()