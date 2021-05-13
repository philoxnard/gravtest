#!/usr/bin/python

"""
Client code that interacts with the web server over Websockets

Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

"""

import json
from websocket import create_connection

WEBSOCKET_URL_TEMPLATE = "ws://%s/ws1.ws"

class GravityWebsocketApi():

	def __init__(self, gravityIP):

		self.gravity_ip = gravityIP
		self.gravity_websocket_url = WEBSOCKET_URL_TEMPLATE % self.gravity_ip

		self.ws = create_connection( self.gravity_websocket_url )

	def sendMessage(self, message):

		message_str = json.dumps( message )

		print "Sending: %s" % message_str
		self.ws.send(message_str)

	def receiveMessage(self):

		result =  self.ws.recv()
		print "Received '%s'" % result

		return result

	def closeWebsocket(self):
		self.ws.close()

	def websocketTest(self):

		message = {}
		message["command"] = "ajax_test"
		message["value"] = "TEST1234"

		self.sendMessage( message )
		result = self.receiveMessage()

		return result

if __name__ == "__main__":

	gravity_api = GravityWebsocketApi( "localhost" )
	gravity_api.websocketTest()