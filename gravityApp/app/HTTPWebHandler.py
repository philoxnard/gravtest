'''
The MIT License (MIT)

Copyright (C) 2014, 2015 Seven Watt <info@sevenwatt.com>
<http://www.sevenwatt.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

import json
from SimpleHTTPServer import SimpleHTTPRequestHandler
import struct
from base64 import b64encode
from hashlib import sha1
from mimetools import Message
import os
import posixpath
from StringIO import StringIO
import errno, socket #for socket exceptions
import threading
import urllib
import re
import sys

# **** Local Imports ****
from FileSystemTools import *
from GravityConfiguration import *
from GravityRoutes import *
from JsonMessage import *
from MessageParser import *
from LogHelper import *
from UploadFileHandlers import *
from UserManagement import *

DEBUG_FILE_UPLOAD = False
PROCESS_UPLOAD_FILE = True

ENFORCE_LOGIN = True  # This enforces the login, if set to false, user can access all pages.

# This whitelist is a list of files that can be served to a client without being logged in.
#  We need this to display and style the login page. Only used when ENFORCE_LOGIN is True.
WHITE_LIST = [ "/",
			"/about",
			"/admin/login",
			"/admin/register",
			"/admin/forgot-password",
			"/avwatch",
			"/contributors",
			"/home",
			"/features",
			"/forgot-password",
			"/index",
			"/index.html",
			"/index.html",
			"/events",
			"/email_list",
			"/blog",
			"/checkout",
			"/checkout.html",
			"/checkout/success",
			"/dashboard",
			"/dashboard.html",
			"/landing",
			"/landing.html",
			"/register",
			"/register.html",
			"/welcome",
			"/favicon.ico",
			"/vendor/fontawesome-free/css/all.min.css",
			"/vendor/magnific-popup/magnific-popup.css",
			"/css/creative.min.css",
			"/vendor/jquery/jquery.min.js",
			"/img/portfolio/thumbnails/1.jpg",
			"/img/portfolio/thumbnails/2.jpg",
			"/img/portfolio/thumbnails/3.jpg",
			"/img/portfolio/thumbnails/4.jpg",
			"/img/portfolio/thumbnails/5.jpg",
			"/img/portfolio/thumbnails/6.jpg",
			"/img/logo/gravity_logo_transparent.png",
			"/vendor/bootstrap/js/bootstrap.bundle.min.js",
			"/vendor/bootstrap/js/bootstrap.bundle.min.js.map",
			"/vendor/jquery-easing/jquery.easing.min.js",
			"/js/creative.min.js",
			"/vendor/magnific-popup/jquery.magnific-popup.min.js",
			"/js/ajax.js",
			"/js/stripe/checkout.js",
			"/js/stripe/elements.js",
			"/js/auth.js",
			"/js/events/events.js",
			"/js/websocket.js",
			"/vendor/fontawesome-free/css/all.min.css",
			"/css/creative.min.css",
			"/css/login.css",
			"/css/stripe-elements.css",
			"/css/admin/sb-admin-2.min.css",
			"/css/landing/landing-page.min.css",
			"/js/admin/sb-admin-2.min.js",
			"/js/login.js",
			"/register.html",
			"/vendor/magnific-popup/magnific-popup.css",
			"/vendor/jquery/jquery.min.js",
			"/img/portfolio/thumbnails/1.jpg",
			"/img/portfolio/thumbnails/2.jpg",
			"/vendor/bootstrap/js/bootstrap.bundle.min.js",
			"/vendor/jquery-easing/jquery.easing.min.js",
			"/vendor/magnific-popup/jquery.magnific-popup.min.js",
			"/js/creative.min.js",
			"/js/ajax.js",
			"/js/auth.js",
			"/img/portfolio/thumbnails/4.jpg",
			"/js/websocket.js",
			"/img/landing/bg-masthead.jpg",
			"/img/landing/bg-showcase-1.jpg",
			"/img/landing/bg-showcase-2.jpg",
			"/img/landing/bg-showcase-3.jpg",
			"/img/landing/testimonials-1.jpg",
			"/img/landing/testimonials-2.jpg",
			"/img/landing/testimonials-3.jpg",
			"/img/portfolio/thumbnails/3.jpg",
			"/img/portfolio/thumbnails/5.jpg",
			"/img/portfolio/thumbnails/6.jpg",
			"/img/unsplash/mark-basarab-1OtUkD_8svc-unsplash.jpg",
			"/img/unsplash/jakob-dalbjorn-cuKJre3nyYc-unsplash.jpg",
			"/img/unsplash/fn_BT9fwg_E/60x60",
			"/img/unsplash//AU4VPcFN4LE/60x60",
			"/img/unsplash/CS2uCrpNzJY/60x60",
			"/img/unsplash/Mv9hjnEUHR4/60x60",
			"/img/unsplash/QAB-WJcbgJk/60x60",
			"/img/unsplash/K4mSJ7kc0As/600x800",
			"/img/unsplash/Mv9hjnEUHR4/600x800",
			"/img/unsplash/oWTW-jNGl9I/600x800",
			"/vendor/bootstrap/css/bootstrap.min.css",
			"/vendor/fontawesome-free/webfonts/fa-solid-900.woff2",
			"/vendor/simple-line-icons/css/simple-line-icons.css",
			"img/unsplash/tranquilo-stones.jpg" ]

# Admin White List
BASE_PATH_WHITE_LIST = [ "/blog", "/event" ]

# This white list allows anything with this base path to pass
ADMIN_PATH_WHITE_LIST = [ "/login", "/login.html", "/admin/login", "/admin/login.html" ]

class WebSocketError(Exception):
	pass

class HTTPWebHandler(SimpleHTTPRequestHandler):

	_ws_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
	_opcode_continu = 0x0
	_opcode_text = 0x1
	_opcode_binary = 0x2
	_opcode_close = 0x8
	_opcode_ping = 0x9
	_opcode_pong = 0xa

	mutex = threading.Lock()

	# TODO: This could be handled better.  But set http protocol, but if this is being
	#       used with https, you should change this variable to "https" in the calling class.
	protocol = "http"

	# **** Websocket Specific Code ****
	def on_ws_message(self, message):

		"""Override this handler to process incoming websocket messages."""
				# Check what type of data we are receiving
		if self.opcode == TEXT_DATA_OPCODE:

			# This is the main processing of messages being received to be handled.  Most
			#  work is done inside of parseMessage and just a response is created.  There is
			#  a special case below for uploading files over the websocket.  TODO: We could
			#  probably fix this by making JsonMessage a member variable of this class rather than static functions.
			message_response = MessageParser.parseMessage(message, None, self.logger)

			# TODO: We should send an error message here because we couldn't handle the message.
			self.send_message( json.dumps(message_response) )

	def on_ws_connected(self):
		"""Override this handler."""
		pass

	def on_ws_closed(self):
		"""Override this handler."""
		pass

	# **** END Websocket Specific Code ****

	def send_message(self, message):
		self._send_message(self._opcode_text, message)

	def setup(self):
		SimpleHTTPRequestHandler.setup(self)
		self.connected = False

	# def finish(self):
		# #needed when wfile is used, or when self.close_connection is not used
		# #
		# #catch errors in SimpleHTTPRequestHandler.finish() after socket disappeared
		# #due to loss of network connection
		# try:
			# SimpleHTTPRequestHandler.finish(self)
		# except (socket.error, TypeError) as err:
			# self.log_message("finish(): Exception: in SimpleHTTPRequestHandler.finish(): %s" % str(err.args))

	# def handle(self):
		# #needed when wfile is used, or when self.close_connection is not used
		# #
		# #catch errors in SimpleHTTPRequestHandler.handle() after socket disappeared
		# #due to loss of network connection
		# try:
			# SimpleHTTPRequestHandler.handle(self)
		# except (socket.error, TypeError) as err:
			# self.log_message("handle(): Exception: in SimpleHTTPRequestHandler.handle(): %s" % str(err.args))

	def checkAuthentication(self):

		auth = self.headers.get('Authorization')
		if auth != "Basic %s" % self.server.auth:
			self.send_response(401)
			self.send_header("WWW-Authenticate", 'Basic realm="Plugwise"')
			self.end_headers();
			return False
		return True

	def isPathAllowed(self, path):
		"""
		This function checks if the path specified is allowed to be returned based on the White List.

		TODO: Also check based on authentication.
		"""

		if path == "":
			return True

		# If we are not logged in but the user requested the login page, give it to them.
		for allowed_admin_path in ADMIN_PATH_WHITE_LIST:
			if allowed_admin_path == path:
				return True

		path_array = path.split("/")

		if len( path_array ) >= 2:
			base_path = "/" + path_array[1]

			for allowed_base_path in BASE_PATH_WHITE_LIST:
				if allowed_base_path == base_path:
					return True

		# Any other paths the user requested must be in the white list.
		for allowed_path in WHITE_LIST:
			if allowed_path == path:
				return True

		return False

	def do_HEAD(self):
		"""
		The Base class only supports do_GET, do_HEAD, and do_POST
		This function gets called from handle_one_request inside of BaseHTTPServer.py

		Returns a 501 code, which means Not Implemented, the server 
		does not support the functionality required to fulfill the request.

		TODO: Check for other methods and make sure nothing else is supported
		"""
		self.send_error(501, "Unsupported method HEAD")

	def do_GET(self):

		# Check if there is any base paths that we should be letting through
		#  because sometimes we want a path with sub-paths to pass.
		# TODO: Inside of this new object, we should also have any URL parameters that were passed.
		#       In the future only parse the URL once and then pass this into the controller.
		parsed_path = GravityRoutes.parseUrl( self.path )

		# First check if we are trying to upgrade this connection to a websocket.
		if self.headers.get("Upgrade", None) == "websocket":
			"""Upgrade connection to a websocket connection"""

			self._handshake()

			#This handler is in websocket mode now.
			#do_GET only returns after client close or socket error.
			self._read_messages()

		elif ENFORCE_LOGIN == False:
			# Enforce login disabled, just allow them to access anything they want to.
			self.do_GET_CUSTOM( parsed_path )

		elif self.headers.getheader('Authorization') == None:
			# If we didn't receive an Authorization field in the header, first check if there is a JWT
			# in a cookie to see this request is validated.

			if self.headers.getheader('Cookie') != None:
				# If there is no Authorization field in the header, check if there is a token present in a Cookie

				# TODO: Based on RFC 6750, it may not be secure to store a bearer token in a cookie because the cookies
				#  could be sent in the clear, possibly making the site in-secure.  We may want to change this.
				cookies = self.headers.getheader('Cookie')
				cookies_array = cookies.split(" ")

				for cookie in cookies_array:
					cookie_array = cookie.split("=")

					if len(cookie_array) == 2 and cookie_array[0] == "token":
						# If we find a token and it is a valid token that we generated for the client, we can
						#  serve them the page they are requesting.

						token = cookie_array[1]

						if UserManagement.validateToken(token):
							if self.path == "/":
								self.do_REDIRECT("/index.html")
							else:
								self.do_GET_CUSTOM( parsed_path, token )
							return

			# Strip off any trailing "/"
			path = parsed_path.path.rstrip("/")

			if self.isPathAllowed( path ):
				"""
				Check if this path is allowed to be returned to the user.
				"""
				self.do_GET_CUSTOM( parsed_path )
				return
			else:

				# If we got here, it means the path that was requested was not one we know about
				#  and we are also not logged in, redirect them to the login page.
				self.do_LOGIN()
				return

		elif self.headers.getheader('Authorization') != None:

			# Check for any bearer tokens, if found check if token is present and serve page.
			header_auth_array = self.headers.getheader('Authorization').split( " ", 1 )

			if len(header_auth_array) == 2 and header_auth_array[0].lower() == "bearer":
				# We have received a request with a JWT.  Validate the token is valid and then serve
				#  them the web page.

				token = header_auth_array[1]
				if self.do_VALIDATE_TOKEN(token):
					self.do_GET_CALL()
					return

		else:
			print("Error: We should not have come here.")

	def do_GET_CUSTOM(self, parsedPath, token=None):
		"""
		Returns a custom page to the client based on a controller that does server-side templating.

		TODO: I'm not trilled with how I'm doing this here.  Do research on how other frameworks handle this.
		"""

		# Check if this path matches a path we have configured for one of the controllers.
		controller = GravityRoutes.getController( parsedPath )

		if controller != None:
			self.do_GET_TEMPLATE( controller, token )
		else:
			# Check if this is a directory request, if so block it.
			if self.path[len(self.path)-1] == "/":
				print("found directory request, not returning")
			else:
				# If we didn't find a controller, just do a normal GET.
				self.do_GET_CALL()

	def do_GET_CALL(self):
		"""
		This function is here because the super class do_GET function allows
		directory access, which we don't want to support for security reasons.
		So any paths that end with /, except for logs we are going to prevent.
		"""

		if self.path.endswith("/"):
			# Since the base class allows directory access and we don't
			#  want that to happen, block it if we have "/" at end of path.
			self.send_error(404, "File not found")
		else:
			SimpleHTTPRequestHandler.do_GET(self)

	def do_GET_TEMPLATE(self, controller=None, token=None):
		"""
		This function takes in a controller function that has been determined by GravityRoutes
		and sends the rendered HTML template back to the client. If token is present, we look
		up the username (email) that is associated with that token before we call the contoller
		function, as there might be some user specific behavior for the template we are requesting.
		"""

		if controller == None:
			print("Error, we need a controller")
			return

		current_username = None
		if token != None:
			current_username = self.do_GET_USERNAME( token )

		if current_username != None:
			body = controller( self.path, current_username)
		else:
			body = controller( self.path )

		# We now have the rendered HTML body from the controller, send it to the client.
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.send_header("Content-length", len(body))
		self.end_headers()
		self.wfile.write(body.encode('utf-8').strip())

	def do_GET_TOKEN(self):
		"""
		This function gets the token from the clients request.
		The token could be in a Cookie or in the Authorization field as a bearer token.

		TODO: I think there there a bug with this function where it wouldn't find the correct token, need to check.
		"""

		if self.headers.getheader('Cookie') != None:
			# If there is no Authorization field in the header, check if there is a token present in a Cookie

			# TODO: Based on RFC 6750, it may not be secure to store a bearer token in a cookie because the cookies
			#  could be sent in the clear, possibly making the site in-secure.  We may want to change this.
			cookies = self.headers.getheader('Cookie')
			cookies_array = cookies.split(" ")

			for cookie in cookies_array:
				cookie_array = cookie.split("=")

				if len(cookie_array) == 2 and cookie_array[0] == "token":
					# If we find a token and it is a valid token that we generated for the client, we can
					#  serve them the page they are requesting.

					token = cookie_array[1]
					return token

		elif self.headers.getheader('Authorization') != None:

			# Check for any bearer tokens, if found check if token is present and serve page.
			header_auth_array = self.headers.getheader('Authorization').split( " ", 1 )

			if len(header_auth_array) == 2 and header_auth_array[0].lower() == "bearer":
				# We have received a request with a JWT.  Validate the token is valid and then serve
				#  them the web page.

				token = header_auth_array[1]
				return token

		return None

	def do_GET_USERNAME(self, token):
		"""
		This function finds the user that just make this request based on the token they submitted.
		"""
		issued_tokens = JsonFile.readJsonFile( GravityConfiguration.getTokensFilePath() )

		if issued_tokens == None:
			return None

		# Now we are going to check if the token the client just sent is one of our issued tokens.
		if token in issued_tokens:
			# TODO: We should actually decode the token here and check that it is valid and hasn't expired.
			return issued_tokens[token]

		return None

	def do_HOME(self):

		host = self.headers.getheader('Host')

		redirect_location = self.protocol + '://%s%s' % (host, "/index.html")

		self.send_response(301)
		self.send_header('Location', redirect_location)
		self.end_headers()

	def do_LOGIN(self):
		"""
		This function just redirects the client to the login page.
		"""
		host = self.headers.getheader('Host')

		# How do we check the protocol?
		redirect_location = self.protocol + '://%s%s' % (host, "/login.html")

		self.send_response(301)
		self.send_header('Location', redirect_location)
		self.end_headers()

	def do_POST(self):
		"""Serve a POST request."""

		handle_post_data = False  # Set to False until they pass token validation

		# Content-Length specifies the length of the data in the payload.  Determine
		#  this lenght first so we know how much information to read from the file.
		content_length = int( self.headers.getheader('Content-Length') )
		content_type = self.headers.getheader('Content-Type')

		# If this is an application/json request, we need to handle this request differently.
		if content_type == "application/json":

			# TODO: Does this work if the message is really long?
			message = self.rfile.read( content_length )
			return self.do_HANDLE_POST_JSON( message )

		# If this is not an application/json POST request, continue to process.
		r, info = self.handle_post_data()

		print(r, info, "by: ", self.client_address)

		# Check the result of the how the post data was handled
		#  and if there was an error, send it back to the user
		if r == True:
			"""
			We just want to tell the client that everything with the file upload
			went okay and send them a JSON message back for how to deal with the result.
			"""

			file_path = info
			basepath, filename = os.path.split(file_path)

			# Redirect the user back to the gallery file.
			# TODO: We should have here a check if this was a file upload from an AJAX/API request
			#       because if it is, we should send them a JSON response rather than a redirect
			self.do_REDIRECT( self.path )
			return
		else:
			# Send 500 that there was an error
			message_response = JsonMessage.createErrorMessage( "reply", "upload_complete", "File could not be written" )
			self.do_SEND_JSON_RESPONSE( message_response )
			return

	def do_HANDLE_POST_JSON(self, message):
		"""
		This function handles messages sent from the client that are specified as application/json
		as the content type.  We handle these messages based on a message schema defined by our API.

		TODO: Just pass in JsonMessage.parseMessage instead of handling explicitly here.
		"""

		options = {}

		# Get the token and pass it to the message handler incase it needs it.
		token = self.do_GET_TOKEN()
		if token != None:
			options = {}
			options["token"] = token

		# If the Gravity Server has been launched from a parent thread, status
		#  information from the parent thread is available instead of this object.
		if self.main_thread_status != None:
			options["main_thread_status"] = self.main_thread_status

		# If there is a message queue to send messages to the parent thread, pass it in with the options here.
		if self.message_queue != None:
			options["message_queue"] = self.message_queue

		if PRINT_API_REQUEST_MESSAGES == True:
			print("Parsing message from client: %s" % message)

		message_response = MessageParser.parseMessage( message, options, self.logger )

		# Now send this response back to the client
		self.do_SEND_JSON_RESPONSE( message_response )
		return

	def do_REDIRECT(self, redirectLocation):
		"""
		This tells the client to redirect to a new location.
		"""
		host = self.headers.getheader('Host')

		redirect_location = self.protocol + '://%s%s' % (host, redirectLocation)

		self.send_response(301)
		self.send_header('Location', redirect_location)
		self.end_headers()

	def do_SEND_JSON_RESPONSE(self, jsonResponse):
		"""
		Takes jsonResponse as a dictionary and writes the response as a JSON string back to the client
		"""

		if PRINT_API_RESPONSE_MESSAGES == True:
			print("Response: %s" % json.dumps(jsonResponse))

		f = StringIO()
		f.write( json.dumps(jsonResponse) )

		length = f.tell()
		f.seek(0)

		self.send_response(201)
		self.send_header("Content-type", "application/json")
		self.send_header("Content-Length", str(length))
		self.end_headers()

		if f:
			self.copyfile(f, self.wfile)
			f.close()

	def handle_post_data(self):
		"""
		Handles the data coming in a POST for file upload
		"""

		# First we need to check if the upload folder exists and if not create it.
		upload_folder_path = GravityConfiguration.getUploadFolderPath()
		upload_folder_path = FileSystemTools.checkAndCreateDirectory( upload_folder_path )

		if upload_folder_path == None:
			return (False, "Cannot create upload folder: %s" % upload_folder_path )

		header_split = self.headers.plisttext.split("=")

		if len(header_split) > 1:
			boundary = header_split[1]
		else:
			print("Could not find boundary, returning")
			return (False, "Could not find the boundary")

		remainbytes = int(self.headers['content-length'])

		line = self.rfile.readline()
		remainbytes -= len(line)

		if not boundary in line:
			return (False, "Content does NOT begin with boundary")

		# Read the information we need to open the file
		remainbytes, file_name = self.read_file_information( remainbytes )

		# Adjust the upload file path incase there was a change to the filename because of
		#  a duplicate file.
		upload_file_path = os.path.join(upload_folder_path, file_name)

		out = self.open_upload_file( upload_file_path )

		if out == None:
			return (False, "Can't create file to write, do you have permission to write?")

		preline = self.rfile.readline()
		remainbytes -= len(preline)

		# Now receive the bytes for the file and write them to the open file descriptor
		while remainbytes > 0:

			line = self.rfile.readline()
			remainbytes -= len(line)

			if boundary in line:
				preline = preline[0:-1]

				if preline.endswith('\r'):
					preline = preline[0:-1]

				out.write(preline)
				out.close()

				# TODO: Move this somewhere better.
				# Might want to wait until the end so all files get uploaded at once,
				#  Then they get processed.
				if PROCESS_UPLOAD_FILE == True:
					result = self.processNewFile( upload_file_path )

				# Return success and the name of the file we just uploaded

				print("File was closed, we have remainbytes = %d" % remainbytes)
				if remainbytes == 0:
					# Here we should probably check if we are done, this won't handle multiple file uploads
					return (True, file_name)
				else:
					# There is still more data to read.
					remainbytes, file_name = self.read_file_information( remainbytes )

					# Adjust the upload file path incase there was a change to the filename because of
					#  a duplicate file.
					upload_file_path = os.path.join(upload_folder_path, file_name)

					out = self.open_upload_file( upload_file_path )

					if out == None:
						return (False, "Can't create file to write, do you have permission to write?")

					preline = self.rfile.readline()
					remainbytes -= len(preline)

			else:
				out.write(preline)
				preline = line

		return (False, "Unexpect Ends of data.")

	def open_upload_file(self, upload_file_path):
		"""
		This function opens the upload file for writing.
		"""

		self.logger.info( "Upload path is = %s" % upload_file_path )

		try:
			self.logger.info( "opening file with path, upload_file_path = %s " % upload_file_path )
			out = open(upload_file_path, 'wb')
			return out

		except IOError:
			return None

	def read_file_information(self, remainbytes):

		# Now start reading the information we need for the upload file
		line = self.rfile.readline()
		remainbytes -= len(line)

		if DEBUG_FILE_UPLOAD == True:
			print( "line (%d) 1: %s" % (len(line), line) )

		fn = re.findall(r'Content-Disposition.*name="(.*)"; filename="(.*)"', line)
		if not fn:
			return (False, "Can't find out file name...")
		else:
			if DEBUG_FILE_UPLOAD == True:
				print(fn)

		input_name = fn[0][0]  # This matches the "name" field in the upload submission form specified in the HTML.
		file_name = fn[0][1]   # This is the actual name of the upload file

		line = self.rfile.readline()
		remainbytes -= len(line)

		#content_type_line = line   # This will look like "Content-Type: image/jpeg"

		if DEBUG_FILE_UPLOAD == True:
			print(( "line (%d) 2: %s" % (len(line), line) ))
			print("input_name = %s, file_name = %s" % ( input_name, file_name ))

		line = self.rfile.readline()
		remainbytes -= len(line)

		if DEBUG_FILE_UPLOAD == True:
			print( "line (%d) 3: %s" % (len(line), line) )

		return remainbytes, file_name

	def _read_messages(self):

		while self.connected == True:
			try:
				self._read_next_message()
			except (socket.error, WebSocketError), e:
				#websocket content error, time-out or disconnect.
				self.log_message("RCV: Close connection: Socket Error %s" % str(e.args))
				self._ws_close()
			except Exception as err:
				#unexpected error in websocket connection.
				self.log_error("RCV: Exception: in _read_messages: %s" % str(err.args))
				self._ws_close()

	def processNewFile(self, filepath):
		"""
		This function processes an uploaded file.  The function just calls
		the function in the UploadFileHandlers class which actually deals with any processing
		of the file.
		"""

		result = UploadFileHandlers.processNewFile( filepath, self.logger )

		return result

	def _read_next_message(self):
		#self.rfile.read(n) is blocking.
		#it returns however immediately when the socket is closed.
		try:
			self.opcode = ord(self.rfile.read(1)) & 0x0F
			length = ord(self.rfile.read(1)) & 0x7F
			if length == 126:
				length = struct.unpack(">H", self.rfile.read(2))[0]
			elif length == 127:
				length = struct.unpack(">Q", self.rfile.read(8))[0]
			masks = [ord(byte) for byte in self.rfile.read(4)]
			decoded = ""
			for char in self.rfile.read(length):
				decoded += chr(ord(char) ^ masks[len(decoded) % 4])
			self._on_message(decoded)
		except (struct.error, TypeError) as e:
			#catch exceptions from ord() and struct.unpack()
			if self.connected:
				raise WebSocketError("Websocket read aborted while listening")
			else:
				#the socket was closed while waiting for input
				self.log_error("RCV: _read_next_message aborted after closed connection")
				pass

	def _send_message(self, opcode, message):

		try:
			#use of self.wfile.write gives socket exception after socket is closed. Avoid.
			self.request.send(chr(0x80 + opcode))
			length = len(message)
			if length <= 125:
				self.request.send(chr(length))
			elif length >= 126 and length <= 65535:
				self.request.send(chr(126))
				self.request.send(struct.pack(">H", length))
			else:
				self.request.send(chr(127))
				self.request.send(struct.pack(">Q", length))
			if length > 0:
				self.request.send(message)

		except socket.error, e:
			#websocket content error, time-out or disconnect.
			self.log_message("SND: Close connection: Socket Error %s" % str(e.args))
			self._ws_close()
		except Exception as err:
			#unexpected error in websocket connection.
			self.log_error("SND: Exception: in _send_message: %s" % str(err.args))
			self._ws_close()

	# ***** Additional Websocket Code ******
	def _handshake(self):

		headers=self.headers

		# Set the protocol version to HTTP/1.1 because RFC6455 states that it must be for a websocket
		#  connection and Safari is more strict about this than some other browsers.
		self.protocol_version = "HTTP/1.1"

		if headers.get("Upgrade", None) != "websocket":
			return
		key = headers['Sec-WebSocket-Key']
		digest = b64encode(sha1(key + self._ws_GUID).hexdigest().decode('hex'))
		self.send_response(101, 'Switching Protocols')
		self.send_header('Upgrade', 'websocket')
		self.send_header('Connection', 'Upgrade')
		self.send_header('Sec-WebSocket-Accept', str(digest))
		self.end_headers()
		self.connected = True
		#self.close_connection = 0
		self.on_ws_connected()

	def _ws_close(self):

		#avoid closing a single socket two time for send and receive.
		self.mutex.acquire()
		try:
			if self.connected:
				self.connected = False
				#Terminate BaseHTTPRequestHandler.handle() loop:
				self.close_connection = 1
				#send close and ignore exceptions. An error may already have occurred.
				try:
					self._send_close()
				except:
					pass
				self.on_ws_closed()
			else:
				self.log_message("_ws_close websocket in closed state. Ignore.")
				pass
		finally:
			self.mutex.release()

	def _on_message(self, message):
		#self.log_message("_on_message: opcode: %02X msg: %s" % (self.opcode, message))

		# close
		if self.opcode == self._opcode_close:
			self.connected = False
			#Terminate BaseHTTPRequestHandler.handle() loop:
			self.close_connection = 1
			try:
				self._send_close()
			except:
				pass
			self.on_ws_closed()
		# ping
		elif self.opcode == self._opcode_ping:
			_send_message(self._opcode_pong, message)
		# pong
		elif self.opcode == self._opcode_pong:
			pass
		# data
		elif (self.opcode == self._opcode_continu or
				self.opcode == self._opcode_text or
				self.opcode == self._opcode_binary):
			self.on_ws_message(message)

	# ***** END Additional Websocket Code ******

	def _send_close(self):

		#Dedicated _send_close allows for catch all exception handling
		msg = bytearray()
		msg.append(0x80 + self._opcode_close)
		msg.append(0x00)
		self.request.send(msg)

	def translate_path(self, path):
		"""This function translates the path that is inside of the html file to
		   a path based on where we have specified the HTML files to be."""

		path = posixpath.normpath(urllib.unquote(path))
		words = path.split('/')
		words = filter(None, words)
		path = self.base_path

		for word in words:
			drive, word = os.path.splitdrive(word)
			head, word = os.path.split(word)
			if word in (os.curdir, os.pardir):
				continue
			path = os.path.join(path, word)

		return path
