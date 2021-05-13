#!/usr/bin/env python

"""
Written by: J. Patrick Farrell
Copyright 2019 Creative Collisions Technology, LLC

JsonMessageCommands.py

This file defines all of the message commands that we currently support.

"""

# **** Message commands ****
COMMAND_AJAX_TEST = "ajax_test"

# Generic commands
COMMAND_LOGIN = "login"
COMMAND_LOGOUT = "logout"

# Blog commands
COMMAND_BLOG_NEW_POST = "blog_new_post"
COMMAND_BLOG_SUBMIT_DELETE = "blog_submit_delete"
COMMAND_BLOG_SUBMIT_EDIT = "blog_submit_edit"

# Event Commands
COMMAND_EVENT_ATTENDEE_CHECKIN = "event_attendee_checkin"
COMMAND_EVENT_ATTENDEE_DELETE = "event_attendee_delete"
COMMAND_EVENT_ATTENDEE_EDIT = "event_attendee_edit"
COMMAND_EVENT_SUBMIT_DELETE = "event_submit_delete"
COMMAND_EVENT_SUBMIT_EDIT = "event_submit_edit"
COMMAND_EVENT_SUBMIT_NEW = "event_submit_new"
COMMAND_EVENT_REGISTER = "event_register"

# Contacts Commands
COMMAND_CONTACT_ADD = "contact_add"
COMMAND_CONTACT_EDIT = "contact_edit"
COMMAND_CONTACT_DELETE = "contact_delete"

# User Management Commands
COMMAND_USER_ADD_NEW = "user_add_new"
COMMAND_USER_DELETE = "user_delete"
COMMAND_USER_EDIT = "user_edit"
COMMAND_USER_EDIT_PASSWORD = "user_edit_password"
COMMAND_USER_LOGOUT = "user_logout"
COMMAND_USER_REGISTER = "user_register"
COMMAND_USER_SET_PASSWORD = "user_set_password"

# Stripe Commands
COMMAND_STRIPE_CHARGE = "stripe_charge_card"
COMMAND_STRIPE_GET_KEYS = "stripe_get_keys"
COMMAND_STRIPE_GET_SESSION = "stripe_get_session"
