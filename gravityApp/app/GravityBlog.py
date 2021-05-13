#!/usr/bin/env python

"""

GravityBlog.py

This file manages the creation of the gravity blog.  This currently is use a single user blog
for now, but in the future the plan is to expand this for every user in the system to be able to have
their own blog.

Written by: J. Patrick Farrell
Copyright 2019

"""

import datetime
import json
import uuid

# **** Local Import ****
from JsonFile import *
from GravityConfiguration import *

class GravityBlog():

	def __init__(self):
		pass

	def createPost(self, blogTitle, blogSubTitle, blogText):
		"""
		This function creates the blog text and saves it within a file called blog.json
		"""

		blog_file_path = GravityConfiguration.getBlogFile()
		current_blog = JsonFile.readJsonFile( blog_file_path )

		if current_blog == None:
			current_blog = {}

		blog_item = {}
		blog_item["datetime_created"] = datetime.datetime.now().ctime()
		blog_item["text"] = blogText
		blog_item["title"] = blogTitle
		blog_item["subtitle"] = blogSubTitle

		# Create the label that we are going to use for the URL.
		# TODO: We need to make this much more robust.
		label = blogTitle.lower().replace(" ", "-")
		label = label.replace("'", "-")
		label = label.replace(",", "-")
		blog_item["label"] = label

		# Create a random ID to idenitfy this event.
		random_id = str(uuid.uuid4()).split("-")[0]
		blog_item["id"] = random_id

		# If this is the first blog item we are adding, we need to create the array to store
		#  all of the posts.
		if "blog_items" not in current_blog:
			current_blog["blog_items"] = []

		current_blog["blog_items"].append( blog_item )

		result = JsonFile.writeJsonFile( current_blog, blog_file_path )

		if result == False:
			reason = "Error: Could not write blog file"
			print(reason)
			return None, reason

		return result

	def deletePost(self, blogLabel):
		"""
		This deletes an event. Cannot be un-done.
		"""

		blog_file_path = GravityConfiguration.getBlogFile()
		current_blog = JsonFile.readJsonFile( blog_file_path )

		if current_blog == None:
			return None

		if "blog_items" not in current_blog:
			reason = "Warning: blog_items not found in blog file."
			print(reason)
			return None

		blog_items = current_blog["blog_items"]

		index = 0
		for blog_item in blog_items:
			if "label" in blog_item and blog_item["label"] == blogLabel:
				print("Deleting blog post %s" % blog_item["title"])
				del blog_items[index]
				break

			index = index + 1

		result = JsonFile.writeJsonFile( current_blog, blog_file_path )

		if result == False:
			reason = "Error: Could not write blog file"
			print(reason)
			return None, reason

		return True, None

	def editPost(self, blogItem):
		"""
		This function edits a blog post that currently exists.
		"""

		blog_file_path = GravityConfiguration.getBlogFile()
		current_blog = JsonFile.readJsonFile( blog_file_path )

		if "label" not in blogItem:
			reason = "Error: Could not edit event because we could not find the blog label in blogItem request"
			print(reason)
			return None, reason

		blog_label = blogItem["label"]

		if current_blog != None and "blog_items" in current_blog:
			blog_items = current_blog["blog_items"]

			for blog_item in blog_items:

				print(blog_item["label"])

				if "label" in blog_item and blog_item["label"] == blog_label:
					# We found the blog item, now edit the settings
					if "title" in blogItem:
						blog_item["title"] = blogItem["title"]

					if "location" in blogItem:
						blog_item["subtitle"] = blogItem["subtitle"]

					if "text" in blogItem:
						blog_item["text"] = blogItem["text"]

					result = JsonFile.writeJsonFile( current_blog, blog_file_path )

					if result == False:
						reason = "Error: Could not write blog file"
						print(reason)
						return None, reason
					else:
						return True, None

	# **** Getters ****
	def getPost(self, blogIdentifier):
		"""
		This gets a particular blog based on the blog identifier.
		The blogIdentifier can be either the blog label or the blog ID.
		"""

		blogs_file_path = GravityConfiguration.getBlogFile()
		gravity_blog_posts = JsonFile.readJsonFile( blogs_file_path )

		if gravity_blog_posts != None and "blog_items" in gravity_blog_posts:
			blog_items = gravity_blog_posts["blog_items"]

			for blog_post in blog_items:
				# First check if the eventIdentifier matches the event ID
				if "id" in blog_post and blog_post["id"] == blogIdentifier:
					return blog_post

				# If we didn't find it based on the ID, check based on the label.
				if "label" in blog_post and blog_post["label"] == blogIdentifier:
					return blog_post

		return None

	def getBlogItems(self):

		blog_file_path = GravityConfiguration.getBlogFile()
		current_blog = JsonFile.readJsonFile( blog_file_path )

		if current_blog != None and "blog_items" in current_blog:
			return current_blog["blog_items"]

		return None

	def getBlogItem(self, blogLabel):
		"""
		This gets a particular event based on the event label.
		"""

		blog_file_path = GravityConfiguration.getBlogFile()
		current_blog = JsonFile.readJsonFile( blog_file_path )

		if current_blog != None and "blog_items" in current_blog:
			blog_items = current_blog["blog_items"]

			for blog_item in blog_items:
				if "label" in blog_item and blog_item["label"] == blogLabel:
					return blog_item

		return None

if __name__ == '__main__':

	gravity_blog = GravityBlog()

	gravity_blog.createPost( "This is the Title", "This is the sub-title", "This is a test" )
