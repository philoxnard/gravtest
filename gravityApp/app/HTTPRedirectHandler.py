'''
The MIT License (MIT)

Copyright (C) 2014, 2015 Seven Watt <info@sevenwatt.com>
<http://www.sevenwatt.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


Note: This file has been modified from its original form to allow the TM1 server
		support an HTTP POST file upload and server files from a custom directory.
--pfarrell

'''

from SimpleHTTPServer import SimpleHTTPRequestHandler
import struct
from hashlib import sha1
import os
import posixpath
from StringIO import StringIO
import errno, socket #for socket exceptions
import threading
import urllib
import re
import json
import platform

class WebSocketError(Exception):
	pass

class HTTPRedirectHandler(SimpleHTTPRequestHandler):
	_ws_GUID = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
	_opcode_continu = 0x0
	_opcode_text = 0x1
	_opcode_binary = 0x2
	_opcode_close = 0x8
	_opcode_ping = 0x9
	_opcode_pong = 0xa

	mutex = threading.Lock()

	def setup(self):
		SimpleHTTPRequestHandler.setup(self)
		self.connected = False

	def do_REDIRECT(self):
		"""
		https://stackoverflow.com/questions/9130422/how-long-do-browsers-cache-http-301s#21396547

		At least two browsers - Chrome and Firefox - will cache a 301 redirect with no expiry date.

		A better alternative in my opinion, however, is to use a 302 or 307 redirect.
		These don't imply to browsers or caches that they are "permanent" redirects and
		thus shouldn't be cached in the absense of Cache-Control headers.
		"""

		host = self.headers.getheader('Host')
		redirect_location = 'https://%s%s' % (host, self.path)

		self.send_response(302)
		self.send_header('Location', redirect_location)
		self.end_headers()

	def do_GET(self):
		# The only thing we do here is a re-direct
		self.do_REDIRECT()

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
