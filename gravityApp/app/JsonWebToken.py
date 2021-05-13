#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

Handles creating and manipulating JSON Web Tokens.

Note that this is not yet a complete implementation of the JSON Web Token RFC 7519
and the implementation needs to be completed.

Defined by RFC 7519
https://datatracker.ietf.org/doc/rfc7519/

"""

import datetime
import json
import jwt

class JsonWebToken():

	@staticmethod
	def encodeClientToken(id, user_id=None):
		"""
		NOTE: Taken from jwt_utils.py 

		Create a new JWT for the specified client.
		JWT's require the following claims be present.
		exp - token expiry date (Time token expires)
		iat - token issued timestamp (Time token created)
		nbf - timestamp indicating when the token can start being used (usually now)
		sub - the `subject` of this token (an optional user_id)
		aud - the audience this token is valid for, our api client (typically the browser client).

		Note: The calling function must keep track of this client object because we will need it to decode the JWT.
		"""
		iat = datetime.datetime.now()
		exp = iat + datetime.timedelta(days=30)
		nbf = iat

		payload = {
			'exp': exp,
			'iat': iat,
			'nbf': nbf,
			'aud': str(id)
		}

		if user_id:
			payload['sub'] = user_id

		return jwt.encode(
			payload,
			str("secret"),
			algorithm='HS256',
			headers=None
		).decode('utf-8')

if __name__ == '__main__':

	token = JsonWebToken.encodeClientToken("1")
	print(token)