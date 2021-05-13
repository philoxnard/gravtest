
Gravity Contacts System
=======================

This sub-system handles adding and managing contacts. Using this sub-system, we have the ability to collect emails, name and phone number and any other contact information through a form or through the API.

The idea of this subsystem is to be able to collect and create an email list, and integrate with other contact
management software out there, such as [The Links App](https://www.thelinksapp.io/).

Data Storage
------------

In the open source version of this project, all of the contacts are stored in a JSON file.  The file contains objects that contain arrays of contacts, which the object key behing a tag for the list name.

The default list is called "general", but if you specify a list name tag, it will create a new list for that list name.

An optional argument of "name" can be included in the list object that offers a description of the list.