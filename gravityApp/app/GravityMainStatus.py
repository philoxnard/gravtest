#!/usr/bin/env python

"""

Written by: J. Patrick Farrell
Copyright 2021 Creative Collisions Technology, LLC

MainStatus.py

This class keeps track of different variables that we need to keep track of the state of the system.

This allows us to store information in the main thread that can be accessed by other threads for operation
and status reporting.

"""


class GravityMainStatus():

	def __init__(self):
		self.server_name = ""
