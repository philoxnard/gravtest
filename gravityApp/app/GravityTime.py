#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2021 Creative Collisions Technology, LLC

GravityTime.py

MIT License

This class handles time commands and makes a few of the datetime
operations easier that we can use to get time values and determine
time differences.

"""

import datetime
import time

class GravityTime():

	@staticmethod
	def timeNow():
		"""
		Returns the time now as an datatime object.
		"""
		time_now = datetime.datetime.utcnow()

		return time_now

	@staticmethod
	def difference(timeObject):
		"""
		This function gets the difference between the time that was passed in and the time now.

		Returns in seconds
		"""

		time_now = GravityTime.timeNow()

		diff = time_now - timeObject

		return long(diff.total_seconds())


	@staticmethod
	def timeNowString():
		"""
		Return the time now as a string
		"""
		time_now = datetime.datetime.utcnow()

		date_time_str = time_now.strftime("%m/%d/%Y, %H:%M:%S")

		return date_time_str

	@staticmethod
	def loadFromString(dateString):

		# Considering date is in dd/mm/yyyy format
		dt_object = datetime.datetime.strptime(dateString, "%m/%d/%Y, %H:%M:%S")

		return dt_object

	@staticmethod
	def timeFromUnixTimeStamp(unixTimeStamp):
		"""
		Loads the time from a unix timestamp, pass in as an integer.
		"""
		date_time = datetime.fromtimestamp(unixTimeStamp)

		return date_time

	@staticmethod
	def getPrintFromUnixTime(unixTime):

		ts = int(unixTime)

		# if you encounter a "year is out of range" error the timestamp
		# may be in milliseconds, try `ts /= 1000` in that case
		print(datetime.datetime.utcfromtimestamp(ts).strftime('%d/%m/%Y %H:%M:%S'))

if __name__ == '__main__':

	time_str = GravityTime.timeNowString()
	print(time_str)

	date_time = GravityTime.loadFromString( time_str )

	time.sleep(4)

	diff_seconds = GravityTime.getTimeDifference( date_time )
	print("diff_seconds = %f" % diff_seconds)

