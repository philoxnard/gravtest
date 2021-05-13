#!/usr/bin/env python
"""

GravityRoutes.py

This file pulls out model data that fills out the views.

Written by: J. Patrick Farrell
Copyright 2019

"""

import json

# **** Local Imports ****
from JsonFile import *

class GravityModels():

	@staticmethod
	def readModel(modelFile):

		json_file = JsonFile.readJsonFile( modelFile )

		return json_file