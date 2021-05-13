#!/usr/bin/env python

"""
UploadFileHandlers.py

This the the middle layer between the HTTP web handlers and any code
that processes uploaded files.

If you have custom modules that should process upload files, you can
call that code from here.  This class is designed to be modified by the user of the class.

By calling custom module code here, this prevents any changes from needing to be made to the HTTP web handler.

Copyright 2019 Creative Collisions Technology, LLC

Written by: J. Patrick Farrell

"""

class UploadFileHandlers():

	@staticmethod
	def processNewFile(filePath, logger=None):
		"""
		This class is where you can call a custom module to process an uploaded file.

		If you needed to do any checks to determine what type of file has been uploaded, you could
		do that here.
		"""

		if logger != None:
			logger.info( "Got a new file %s, what should I do with it?" % filePath )

		return True