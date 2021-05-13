#!/usr/bin/env python
"""

GravityRoutes.py

This file manages Gravity Routes.

Written by: J. Patrick Farrell
Copyright 2019

This file takes in a route (or path), and returns the appropriate conntrollers.

TODO:
Really this needs to be more complete route handling.  The route handler should be able to process something
like this route, /:orgId/reviews/:reviewId/, and then pass the information into the controller.

This way the route parsing is done within this function, then all of the parameters (params)
from the route are passed into the controller where we can do any database look up.

We should also be able to have a Routes class per each path.

"""

try:
	from urllib.parse import urlparse
except ImportError:
	# For Python 2
	from urlparse import urlparse, parse_qs

# **** Local Imports ****
from GravityControllers import *

# **** Route Controller Table Definitions ****
# These tables define what route maps to which controller.  There are tables
# defined per base path, such that /admin/<path> has a different table than the default
# controller.

ROUTE_CONTROLLER_TABLE = {
	"routes" : {
		"" : {
			"controller" : GravityControllers.home,
		},
		"about" : {
			"controller" : GravityControllers.about,
		},
		"admin" : {
			"controller" : GravityControllersAdmin.admin,
		},
		"blog" : {
			"controller" : GravityControllers.blog,
			"routes" : {
				"newpost" : {
					"controller" : GravityControllers.blogNewPost
				}
			}
		},
		"dashboard" : {
			"controller" : GravityControllers.dashboard,
		},
		"email_list" : {
			"controller" : GravityControllers.emailList,
		},
		"contributors" :{
			"controller" : GravityControllers.contributors,
		},
		"avwatch" : {
			"controller" : GravityControllers.avwatch,
		},
		"event" : {
			"controller" : GravityControllers.event,
			"routes" : {
				"edit" : {
					"controller" : GravityControllers.eventEdit
				},
				"register" : {
					"controller" : GravityControllers.eventRegister
				},
				"confirmed" : {
					"controller" : GravityControllers.eventConfirmed
				}
			}
		},
		"events" : {
			"controller" : GravityControllers.events,
			"routes" : {
				"manage" : {
					"controller" : GravityControllers.eventEdit
				},
				"new" : {
					"controller" : GravityControllers.eventEdit
				}
			}
		},
		"features" : {
			"controller" : GravityControllers.features
		},
		"forgot-password" : {
			"controller" : GravityControllers.forgotPassword
		},
		"home" : {
			"controller" : GravityControllers.home
		},
		"index" : {
			"controller" : GravityControllers.home
		},
		"login" : {
			"controller" : GravityControllers.login
		},
		"landing" : {
			"controller" : GravityControllers.landing
		},
		"welcome" : {
			"controller" : GravityControllersMember.welcome
		},
		"register" : {
			"controller" : GravityControllers.register
		},
		"checkout" : {
			"controller" : GravityControllers.stripeCheckout,
			"routes" : {
				"success" : {
					"controller" : GravityControllers.stripeCheckoutSuccess
				}
			}
		},
		"upload" : {
			"controller" : GravityControllers.upload
		}
	}
}

# Table specifically for the /admin route.
ADMIN_ROUTE_CONTROLLER_TABLE = {
	"routes" : {
		"admin" : {
			"controller" : GravityControllersAdmin.admin,
		},
		"" : {
			"controller" : GravityControllersAdmin.admin,
		},
		"blog" : {
			"routes" : {
				"edit" : {
					"controller" : GravityControllersAdmin.blogEdit
				},
				"new" : {
					"controller" : GravityControllersAdmin.blogNew
				},
				"manage" : {
					"controller" : GravityControllersAdmin.blogManage
				}
			}
		},
		"contacts" : {
			"routes" : {
				"manage" : {
					"controller" : GravityControllersAdmin.contactsManage
				},
			}
		},
		"event" : {
			"routes" : {
				"registrations" : {
					"controller" : GravityControllersAdmin.eventRegistrations
				},
			}
		},
		"events" : {
			"routes" : {
				"edit" : {
					"controller" : GravityControllersAdmin.eventEdit
				},
				"new" : {
					"controller" : GravityControllersAdmin.eventNew
				},
				"manage" : {
					"controller" : GravityControllersAdmin.eventsManage
				}
			}
		},
		"forgot-password" : {
			"controller" : GravityControllersAdmin.forgotPassword
		},
		"login" : {
			"controller" : GravityControllersAdmin.login
		},
		"register" : {
			"controller" : GravityControllersAdmin.register
		},
		"users" : {
			"routes" : {
				"manage" : {
					"controller" : GravityControllersAdmin.usersManage
				}
			}
		}
	}
}

class GravityRoutes():

	@staticmethod
	def parseUrl(path):
		"""
		Use urlparse to parse the path
		"""

		parsed_path = urlparse( path )

		return parsed_path

	@staticmethod
	def getController(parsedPath):
		"""
		This function determines which controller needs to be returned, if a controller doesn't
		match the path, then return None.

		When the user wants to add a new controller for a new route, they need to add a new path to this
		function and they need to add a new controller function to the GravityControllers class.

		TODO: This should be a dictionary or some data structure to make this cleaner.
		"""

		path = parsedPath.path

		# Strip off any trailing "/" from the path.
		if path != "/":
			path = parsedPath.path.rstrip("/")
		else:
			path = path

		path_array = path.split( "/" )

		# Delete the first element which is because of the first "/"
		if len( path_array ) >= 2:
			del path_array[0]

		path_base = path_array[0]

		# Before we can determine which controller needs to be used, we need to strip off the ".html"
		# from the path if it is present.
		path_end = path_array[len(path_array) - 1].split(".html")[0]

		path_index = 0

		if len(path_array) == 1:
			path_base = path_end

		ROUTE_OBJECTS_LUT = ROUTE_CONTROLLER_TABLE["routes"]

		# First check if this is an admin route, if so, set to the Admin table instead of the default route
		#  table.
		# TODO: Somehow make this easier to switch between so if we had say a table for routes with /members, it
		#       would be able to switch to that easily.
		if path_base == "admin":

			ROUTE_OBJECTS_LUT = ADMIN_ROUTE_CONTROLLER_TABLE["routes"]

			# If this is the admin,
			if len( path_array ) >= 2:
				del path_array[0]
				path_base = path_array[0]

		if path_base in ROUTE_OBJECTS_LUT:
			"""
			Note that this only handles one level of sub-routes right now,
			we will want to make more and make this recursive?
			"""

			route_object = ROUTE_OBJECTS_LUT[path_base]

			# Check if this object has its own route object, if so, return the appropriate controller.
			if len(path_array) > 1 and "routes" in route_object:

				path_element = path_array[1]

				if path_element in route_object["routes"]:
					return route_object["routes"][path_element]["controller"]
				else:
					# If we couldn't find the path location in the routes object, return the controller
					#  if we have one.
					# NOTE: This means that we can't have a route like "/events/events" because it would
					#       return the wrong controller.
					if "controller" in route_object:
						return route_object["controller"]

					return None

			elif "controller" in route_object:
				# If there was no routes object, but there was a controllers object, return it.
				return route_object["controller"]
			else:
				return None
		else:
			return None

if __name__ == '__main__':

	#o = urlparse('/index?i=main&mode=front')
	#o = urlparse('/admin?test=test1')
	#o = urlparse('/admin?asfdjksdaf243rjkdjkg')
	#o = urlparse('/events/test/123')
	#o = urlparse('https://localhost/?fbclid=IwAR1HScyEnIUD5mrBXWiDKB_f1EHJpKqmR5pgJ3zdNrsmsRAFVjYFxqsPELY')
	#print o

	#print o.scheme
	#print "path= " + o.path
	#print parse_qs(o.query)
	print(ROUTE_CONTROLLER_TABLE[""]["test"])

