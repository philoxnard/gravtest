
JSON Schema
===========

One of the core featues of Gravity is that it's largely based around passing and storing data in JSON forat. The JSON messages and storage files must follow a particular schema for them to be valid and read by the program.

We define these schemas within the "schemas" folder and then use a validation module within the code to make sure that
all information conforms to the the schema

JSON Schema Validation
----------------------

To validate a JSON config file from the command line, we can use the jsonschema program.  Any time a new message or command is added to a JSON message, the schema file should be updated.  This allows us to keep track of the format of our messages, and also allows us to validate that messages passing through the system conform to the JSON schema.

	$ jsonschema -i config.json config.schema
