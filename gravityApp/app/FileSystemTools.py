#!/usr/bin/env python

"""
FileSystemTools.py: Media Manager server that handles websockets.

Copyright 2019 Creative Collisions Technology, LLC
Written by: J. Patrick Farrell

"""

import os

class FileSystemTools():

	@staticmethod
	def checkAndCreateDirectory(directory):
		"""
		This function just takes in a folder directory and doesn't do an manipulation of
		the path that was passed, but tries to create the directory on disk if it doesn't exist.
		ex. ../../public/nmf_files
		"""

		try:
			os.makedirs(directory)
		except OSError:
			if not os.path.isdir(directory):
				return None

		return directory