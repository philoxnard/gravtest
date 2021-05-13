#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

These are the controllers that render specific HTML templates for the application routes.

This is server-side functionality allows someone to create a template and configure the HTML that is sent
back to the user.

All server-side renderings where we need to pull information from the database before we send
the template back to the client are done in these classes.

"""

import datetime
from jinja2 import Environment, FileSystemLoader # Templating Engine
import os
import json

# **** Local Includes ****
from GravityBlog import *
from GravityContacts import *
from GravityEvents import *
from GravityConfiguration import *
from GravityModels import *
from UserManagement import *

env = Environment(
	loader=FileSystemLoader(VIEWS_ROOT_DIRECTORY)
)

class GravityControllersAdmin():
	"""
	This class is for controllers on the administrator part of the site.

	Note: For any page that requires the user to be logged in, we need to call
		the getContext function so we have information about the permissions this user has.

	TODO: Create a render_template for admins that checks if this user is an admin before returning.
	"""

	@staticmethod
	def getContext(path, currentUser):

		context = {}

		# TODO: We should look up the username and password
		context["current_user"] = currentUser

		if UserManagement.isAdmin( currentUser ) == True:
			context["admin"] = True

		return context

	@staticmethod
	def admin(path, currentUser=None):
		"""
		Gets the admin template.
		"""

		context = GravityControllersAdmin.getContext( path, currentUser )

		return GravityControllers.render_template( "gravity/admin/index.j2", context )

	@staticmethod
	def login(path, currentUser=None):
		"""
		Gets the admin template.
		"""
		return GravityControllers.render_template( "gravity/admin/auth/login.j2" )

	@staticmethod
	def register(path, currentUser=None):
		"""
		Gets the admin template.
		"""
		return GravityControllers.render_template( "gravity/admin/auth/register.j2" )

	@staticmethod
	def forgotPassword(path, currentUser=None):
		"""
		Gets the admin template.
		"""
		return GravityControllers.render_template( "gravity/admin/auth/forgot-password.j2" )

	@staticmethod
	def blogManage(path, currentUser=None):

		context = GravityControllersAdmin.getContext( path, currentUser )

		gravity_blog = GravityBlog()
		blog_items = gravity_blog.getBlogItems()

		if blog_items == None:
			blog_items = []

		context["blog_items"] = blog_items

		return GravityControllers.render_template( "gravity/admin/blog/manage.j2", context )

	@staticmethod
	def blogNew(path, currentUser=None):

		context = GravityControllersAdmin.getContext( path, currentUser )

		return GravityControllers.render_template( "gravity/admin/blog/new.j2", context )

	@staticmethod
	def blogEdit(path, currentUser=None):
		"""
		Gets the page to edit an event for the administrator.
		"""

		context = GravityControllersAdmin.getContext( path, currentUser )

		gravity_blog = GravityBlog()

		path_array = path.split( "/" )

		if len( path_array ) >= 3:
			path = path_array[2]
			blog_label = path_array[4]

			blog_item = gravity_blog.getBlogItem( blog_label )
		else:
			blog_item = None

		if blog_item == None:
			blog_item = {}

		context["blog_item"] = blog_item

		return GravityControllers.render_template( "gravity/admin/blog/edit.j2", context )

	# **** Contact Functions ****
	@staticmethod
	def contactsManage(path, currentUser=None):

		context = GravityControllersAdmin.getContext( path, currentUser )

		gravity_contacts = GravityContacts()
		contact_list = gravity_contacts.contactsGet()

		if contact_list == None:
			contact_list = {}

		context["contact_list"] = contact_list

		return GravityControllers.render_template( "gravity/admin/contacts/manage.j2", context )

	# **** Event Functions ****

	@staticmethod
	def eventsManage(path, currentUser=None):

		context = GravityControllersAdmin.getContext( path, currentUser )

		gravity_events = GravityEvents()
		event_items = gravity_events.getEventItems()

		if event_items == None:
			event_items = []

		context["event_items"] = event_items

		return GravityControllers.render_template( "gravity/admin/events/manage.j2", context )

	@staticmethod
	def eventNew(path, currentUser=None):

		context = GravityControllersAdmin.getContext( path, currentUser )

		return GravityControllers.render_template( "gravity/admin/events/new.j2", context )

	@staticmethod
	def eventEdit(path, currentUser=None):
		"""
		Gets the page to edit an event for the administrator.
		"""

		context = GravityControllersAdmin.getContext( path, currentUser )

		gravity_events = GravityEvents()

		path_array = path.split( "/" )

		if len( path_array ) >= 3:
			path = path_array[2]
			event_label = path_array[4]

			event = gravity_events.getEvent( event_label )
		else:
			event = None

		if event == None:
			event = {}

		context["event"] = event

		return GravityControllers.render_template( "gravity/admin/events/edit.j2", context )

	@staticmethod
	def eventRegistrations(path, currentUser=None):
		"""
		Gets the page of attendee registrations for a particular event.
		"""

		context = GravityControllersAdmin.getContext( path, currentUser )

		gravity_events = GravityEvents()

		path_array = path.split( "/" )

		if len( path_array ) >= 3:
			path = path_array[2]
			event_identifier = path_array[4]

			event_registrations_list = gravity_events.getEventRegistrationList( event_identifier )

		else:
			event_registrations_list = None

		if event_registrations_list == None:
			event_registrations_list = {}

		context["event_registrations_list"] = event_registrations_list
		context["event_identifier"] = event_identifier

		return GravityControllers.render_template( "gravity/admin/events/event_registrations.j2", context )


	@staticmethod
	def usersManage(path, currentUser=None):
		"""
		Gets the page to manage users as an administrator.
		"""

		context = GravityControllersAdmin.getContext( path, currentUser )

		user_items = UserManagement.getCredentials()

		if user_items == None:
			user_items = []

		context["user_items"] = user_items

		return GravityControllers.render_template( "gravity/admin/users/manage.j2", context )


# This class controls all of the Member page renders
class GravityControllersMember():
	"""
	TODO: These functions will check if a user is logged in before continuing to a member-only page.

	Note: This is kind of a double check for these pages because the HTTPWebHandler.py already checks
	      if the person requesting access is a user. The difference now is that we need to disguish between
		  who is a member user and who is an admin, which is why this controller is here.  Need to work out 
		  how the check in the HTTPWebHandler should work with the check inside of this function.
		  Maybe the check should be in the admin controllers instead of here since I'm not sure you can get
		  here without doing a check if the user has an account. Or maybe all of the member account checks for pages
		  should move inside of these controllers and only basic resources should be put in the white list? 
		  But that being said, the difference is too that pages that pass the while list are allowed to make it here, 
		  so this would be a secondary check. Need to work out a bit more about the architecture of this system.
	"""

	@staticmethod
	def getContext(path, currentUser):

		context = {}

		# Check if we have a currentUser and if the user is a member of the system.
		if currentUser != None:
			context["current_user"] = currentUser

			# Check if this user is a registered member of the system.
			if UserManagement.isMember( currentUser ) == True:
				context["member"] = True

		return context

	@staticmethod
	def render_template(templateFile, context=None):
		"""
		Returns the appropriate template based on if the user is logged in or not to the system.
		"""

		if context == None:
			context = {}

		if "member" not in context or context["member"] == False:
			return env.get_template( "gravity/member/not_logged_in.j2" ).render()

		# We now know that the user is registered inside of the system, return template.
		return env.get_template(templateFile).render(context)

	@staticmethod
	def welcome(path, currentUser=None):
		"""
		This is the welcome page when a new user logs in or returns to the system.
		"""
		context = GravityControllersMember.getContext( path, currentUser )

		return GravityControllersMember.render_template( "gravity/member/welcome.j2", context )


# This class contains generic controls and all of the controllers that are publically available.
class GravityControllers():

	@staticmethod
	def render_template(templateFile, context=None):

		if context == None:
			context = {}

		return env.get_template(templateFile).render(context)

	@staticmethod
	def home(path, currentUser=None):
		return GravityControllers.render_template( "gravity/index.j2" )

	@staticmethod
	def contributors(path, currentUser=None):
		return GravityControllers.render_template( "gravity/contributors.j2" )

	@staticmethod
	def avwatch(path, currentUser=None):

		avwatch_obj = open("avwatch.txt", "r")

		text = avwatch_obj.readlines()
		avwatch_obj.close()

		context = {}
		context["test"] = text
		return GravityControllers.render_template( "gravity/avwatch.j2", context )

	@staticmethod
	def dashboard(path, currentUser=None):
		return GravityControllers.render_template( "gravity/dashboard.j2" )

	@staticmethod
	def about(path, currentUser=None):

		about_model = GravityModels.readModel( MODELS_ROOT_DIRECTORY + "/about.json" )

		context = {}
		if about_model != None and "paragraphs" in about_model:
			context["paragraphs"] = about_model["paragraphs"]

		return GravityControllers.render_template( "gravity/about.j2", context )

	@staticmethod
	def blog(path, currentUser=None):
		"""
		Gets the page that will display the main blog page or an individual blog
		page if a blog identifier has been passed in the URL.
		"""

		path_array = path.split("/")
		gravity_blog = GravityBlog()

		if len( path_array ) <= 2:
			# Returns the page with all of the blog posts
			blog_items = gravity_blog.getBlogItems()

			if blog_items == None:
				blog_items = []

			context = {
				'blog_items': blog_items
			}

			return GravityControllers.render_template( "gravity/blog/blog.j2", context )
		else:
			# If we have a blog identifier, look up the individual blog post.
			blog_identifier = path_array[2]

			gravity_blog = GravityBlog()
			blog_post = gravity_blog.getPost( blog_identifier )

			if blog_post == None:
				blog_post = {}

			context = {
				'blog_post': blog_post
			}

			return GravityControllers.render_template( "gravity/blog/post.j2", context )

	@staticmethod
	def blogNewPost(path, currentUser=None):
		"""
		Gets the page for a new blog post
		"""

		return GravityControllers.render_template( "gravity/blog/new.j2" )

	# **** Email List Functions ****
	@staticmethod
	def emailList(path, currentUser=None):
		"""
		Show page for user to submit their information to add to an email list.
		"""

		return GravityControllers.render_template( "gravity/email_list.j2" )

	# **** Event Functions ****
	@staticmethod
	def events(path, currentUser=None):
		"""
		Get the blog items from the blog class and returns as a rendered template.

		Note that by doing this here, this means that the blog is currently generated server-side rather
		than client side.
		"""

		gravity_events = GravityEvents()
		event_items = gravity_events.getEventItems()

		if event_items == None:
			event_items = []

		context = {
			'event_items': event_items
		}

		return GravityControllers.render_template( "gravity/events/events.j2", context )

	@staticmethod
	def eventsManage(path, currentUser=None):
		"""
		This allows you to manage the events that you have in the system.
		"""

		gravity_events = GravityEvents()
		event_items = gravity_events.getEventItems()

		if event_items == None:
			event_items = []

		context = {
			'event_items': event_items
		}

		return GravityControllers.render_template( "gravity/events/manage.j2", context )

	@staticmethod
	def event(path, currentUser=None):
		"""
		Gets the page that will display an individual event.
		"""

		path_array = path.split("/")

		if len( path ) <= 2:
			return GravityControllers.render_template( "gravity/events/event.j2" )
		else:
			event_identifier = path_array[2]

			gravity_events = GravityEvents()
			event = gravity_events.getEvent( event_identifier )

			if event == None:
				event = {}

			context = {
				'event': event
			}

			return GravityControllers.render_template( "gravity/events/event.j2", context )

	@staticmethod
	def eventNew(path, currentUser=None):
		"""
		Gets the page for a new blog post
		"""

		return GravityControllers.render_template( "gravity/events/new.j2" )

	@staticmethod
	def eventEdit(path, currentUser=None):
		"""
		Gets the page to edit an event
		"""

		gravity_events = GravityEvents()

		path_array = path.split( "/" )

		if len( path_array ) >= 2:
			path = path_array[1]
			event_label = path_array[3]

			event = gravity_events.getEvent( event_label )
		else:
			event = None

		if event == None:
			event = {}

		context = {
			'event': event
		}

		return GravityControllers.render_template( "gravity/events/edit.j2", context )

	@staticmethod
	def eventRegister(path, currentUser=None):
		"""
		Gets the page for someone to register for the event.
		"""

		gravity_events = GravityEvents()

		path_array = path.split( "/" )

		# First find the event so we can put up information about the event on the page.
		if len( path_array ) >= 3:
			path = path_array[2]
			event_label = path_array[3]

			event = gravity_events.getEvent( event_label )
		else:
			event = None

		if event == None:
			event = {}

		context = {}
		context["event"] = event

		return GravityControllers.render_template( "gravity/events/register.j2", context )

	@staticmethod
	def eventConfirmed(path, currentUser=None):
		"""
		Displays the page used to show confirmation that the user is attending an event and any addtional
		instructions for them.
		"""

		gravity_events = GravityEvents()

		path_array = path.split( "/" )

		# First find the event so we can put up information about the event on the page.
		if len( path_array ) >= 3:
			path = path_array[2]
			event_identifier = path_array[3]

			event = gravity_events.getEvent( event_identifier )
		else:
			event = None

		if event == None:
			event = {}

		context = {}
		context["event"] = event

		return GravityControllers.render_template( "gravity/events/confirmed.j2", context )

	@staticmethod
	def features(path, currentUser=None):

		features_model = GravityModels.readModel( MODELS_ROOT_DIRECTORY + "/features.json" )

		context = {}
		if features_model != None and "bullets" in features_model:
			context["bullets"] = features_model["bullets"]

		return GravityControllers.render_template( "gravity/features.j2", context )

	@staticmethod
	def forgotPassword(path, currentUser=None):
		"""
		TODO: Using admin forgot password for now until we create a user login page.
		"""
		#return GravityControllers.render_template( "auth/forgot-password.j2" )
		return GravityControllers.render_template( "gravity/admin/auth/forgot-password.j2" )

	@staticmethod
	def login(path, currentUser=None):
		"""
		TODO: Using admin login for now until we create a user login page.
		"""
		#return GravityControllers.render_template( "auth/login.j2" )
		return GravityControllers.render_template( "gravity/admin/auth/login.j2" )

	@staticmethod
	def register(path, currentUser=None):
		"""
		TODO: Using admin register for now until we create a user login page.
		"""
		#return GravityControllers.render_template( "auth/register.j2" )
		return GravityControllers.render_template( "gravity/admin/auth/register.j2" )

	@staticmethod
	def upload(path, currentUser=None):
		return GravityControllers.render_template( "gravity/upload.j2" )

	@staticmethod
	def upload():
		return GravityControllers.render_template( "gravity/upload.j2" )

	# **** Landing Page Functions ****
	@staticmethod
	def landing(path, currentUser=None):
		return GravityControllers.render_template( "gravity/landing/index.j2" ).strip()

	# **** Stripe Functions ****

	@staticmethod
	def stripeCheckout(path, currentUser=None):
		return GravityControllers.render_template( "stripe/checkout.j2" ).strip()

	@staticmethod
	def stripeCheckoutSuccess(path, currentUser=None):
		return GravityControllers.render_template( "stripe/success.j2" ).strip()