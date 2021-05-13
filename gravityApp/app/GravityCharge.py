#!/usr/bin/env python

"""

GravityCharge.py

This file manages the execution of API calls to external payment platforms such as Stripe.
Currently this file only contains simple API calls to Stripe.  In the future we were expand
the functionality to include more platforms as well as tap into some of the stronger features
available such as the customers, subscriptions and orders API's.

Written by: Edward Beazer
Copyright 2019

"""

# Package imports
import stripe
import json
import os

# **** Local Import ****
from GravityConfiguration import *
from JsonFile import *
from dotenv import load_dotenv # Loads environmental variables

load_dotenv() # Loads environtment variables

# initialize stripe key.
# If the stripe key is not available, 
# Stripe will return an error code that will get logged in the console.
stripe.api_key = os.getenv('STRIPE_SK')

HOST_URL=os.getenv("HOST_URL")

class GravityCharge():

	def __init__(self):
		pass

	@staticmethod
	def stripeCharge(stripe_token):
		"""
		Takes in a Stripe token created by StripeJS in the front end
		 and attempts to charge it.  Returns an object from Stripe that
		 will inform us if the charge was successful or not
		"""
		token = stripe_token["token"]
		sku = stripe_token["sku"]
		product = GravityCharge.getSkuInfo(sku)

		if product == None:
			print("Could not charge for the product because we couldn't find the sku")
			return None

		charge = stripe.Charge.create(
			amount=product["amount"],
			currency="usd",
			description=product["description"],
			statement_descriptor=product["statement_descriptor"],
			source=token["id"]
		)

		return charge;
	
	@staticmethod
	def stripeCheckout(sku):
		"""
		Takes in a sku string and returns a Stripe session that will be
		 used for Stripe Checkout 
		"""

		product = GravityCharge.getSkuInfo(sku)

		# Stripe Checkout currently does not support statement_descriptor.
		# We must delete this key/value before passing it to Stripe.
		del product["statement_descriptor"]

		# Creates a stripe checkout session
		session = stripe.checkout.Session.create(
			payment_method_types=['card'],
			line_items=[product],
			success_url=HOST_URL + "/checkout/success",
			cancel_url=HOST_URL + "/checkout",
		);

		return session;

	@staticmethod
	def getSkuInfo(sku):
		"""
		Returns product info that will be used for Stripe Charge/Checkout

		TODO: What is an sku? And this shouldn't be hard coded here, this should be all defined in a json
		 file somewhere and this should be generic info.
		"""

		json_sku_products = JsonFile.readJsonFile( STRIPE_SKU_PRODUCTS )

		skuObject = {}

		if sku in json_sku_products:
			return json_sku_products[sku]

		else:
			print("We couldn't find the sku, returning None")
			return None

if __name__ == '__main__':

	# This creates a test file that we can use for products
	skuObjects = {}
	skuObject = {}

	skuObject["name"] = "Harley"
	skuObject["description"] = "An awesome motorcycle"
	skuObject["statement_descriptor"] = "Purchase by Gravity!"
	skuObject["images"] = ["https://images.unsplash.com/photo-1558981285-6f0c94958bb6?ixlib=rb-.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1950&q=80"]
	skuObject["amount"] = 5000
	skuObject["currency"] = "usd"
	skuObject["quantity"] = 1

	skuObjects["sku_123"] = skuObject

	skuObject["name"] = "Bicycle"
	skuObject["description"] = "Get around places"
	skuObject["statement_descriptor"] = "Purchase by Gravity!"
	skuObject["images"] = ["https://images.unsplash.com/photo-1505158498176-0150297fbd7d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=934&q=80"]
	skuObject["amount"] = 4000
	skuObject["currency"] = "usd"
	skuObject["quantity"] = 1

	skuObjects["sku_456"] = skuObject

	JsonFile.writeJsonFile( skuObjects, "./products.json" )