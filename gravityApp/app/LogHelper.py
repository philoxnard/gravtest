#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019

Log Helper

"""

import argparse
import datetime
import json
import logging
import logging.config
from logging.handlers import RotatingFileHandler
import os
import sys

LOG_DIRECTORY = "."

# **** Local Imports ****
from JsonSchemaHelper import *

# For Reference, Logging Levels
# Level	  Numeric value
# CRITICAL        50
# ERROR           40
# WARNING         30
# INFO            20
# DEBUG           10
# NOTSET          0

# Most human readable output is specified to INFO log level, so make sure
#  this is at least higher than INFO level. But it is set the highest value in production
#  because we want the front-end program only to see nomatyk JSON messages
GRAVITY_LOG_LEVEL = 60

# Define variables that other modules can use without having to import logging
DEBUG_LEVEL = logging.DEBUG
INFO_LEVEL = logging.INFO
WARNING_LEVEL = logging.WARNING
ERROR_LEVEL = logging.ERROR
CRITICAL_LEVEL = logging.CRITICAL

VALIDATE_JSON_SCHEMA = False # Set to True to validate messages against schema

class LogHelper():

	def __init__(self, loggerName, filename, logDirectory=LOG_DIRECTORY):

		self.filepath = logDirectory + "/" + filename

		# Make sure our log directory exists before continuing
		try:
			os.makedirs(logDirectory)
		except OSError:
			if not os.path.isdir(logDirectory):
				return None

		# If you wish to include additional information in the log, add it here as
		#  name value pairs in JSON format.
		self.extras = {}

		OUTPUT_FORMAT = '%(asctime)-12s (%(levelname)s, %(name)s): %(message)s'
		#OUTPUT_FORMAT = '{"version":0, "datetime":"%(asctime)-12s", "log_level":"%(levelname)s", "message":%(message)s}'

		# Set the stream to be stdout, default is to send everything to stderr
		logging.basicConfig(level=logging.DEBUG, stream=sys.stdout, format=OUTPUT_FORMAT)

		# This for loop disables all the logging from other modules so we don't get
		#  a bunch of output we don't need.
		for name, logger in logging.root.manager.loggerDict.iteritems():
			logger.disabled=True

		self.logger = logging.getLogger(loggerName)

		# create a file handler
		self.handler = RotatingFileHandler(self.filepath)
		self.handler.setLevel(logging.INFO)

		# Create a formatter to set the logging format
		self.formatter = logging.Formatter(OUTPUT_FORMAT)
		self.handler.setFormatter(self.formatter)

		# Add the handlers to the logger
		self.logger.addHandler(self.handler)

		# TODO: By having this here, this makes it not very generic and can't use by itself normally
		logging.addLevelName( GRAVITY_LOG_LEVEL, "GRAVITY" )
		#logging.Logger.gravity = self.gravity

	def printLoggingFile(self):
		self.info( "Logging file is: %s" % self.filepath )

	def setLoggingLevel(self, loggingLevel):
		self.logger.setLevel(loggingLevel)
		self.handler.setLevel(loggingLevel)

	def debug(self, message):
		self.logger.debug(message, extra=self.extras)

	def info(self, message):
		self.logger.info(message, extra=self.extras)

	def warning(self, message):
		self.logger.warning(message, extra=self.extras)

	def error(self, message):
		self.logger.error(message, extra=self.extras)

	def critical(self, message):
		self.logger.critical(message, extra=self.extras)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--dir', '-d', default=LOG_DIRECTORY, type=str)

	args = parser.parse_args()

	logger = LogHelper( __name__, "test.log", args.dir )
	logger.info("Test this log")

