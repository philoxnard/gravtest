
Run Gravity using Python
========================

These instructions explain how to get Gravity running with python on your host operating system.

Gravity Python Install Procedure
--------------------------------

Depending on which operating system you are deploying Gravity on, the python install instructions will be slightly different.  Check the appropriate file for the correct install instructions for Debian Linux, MacOS, or Windows (TODO).

The following files have all of the instructions for OSX specific installation.  After you have completed the OSX specific installs, continue with the instructions within the document to install the dependencies needed for Gravity on your host OS.

[Debian Linux Instructions](docs/python/gravity_python_linux.md)
[Mac OS Instructions](docs/python/gravity_python_macos.md)

### Install Python Dependencies

There are a few python modules that are required when running the Gravity Server.  You can install them with the pip tool using the following commands.

The following command will install these modules on your host system. These modules are needed on your host system when running the application manually.  However, if you are building with Docker, the Dockerfile's have been configured to install these dependencies automatically.

 	$ pip install bcrypt Jinja2 PyJWT passlib jsonschema stripe python-dotenv


Gravity Python Run Procedure
----------------------------

### Run with python interpreter directly.

When you run with the python interpreter directly, there is no build or compile necessary.  However, your host machine must have all of the python dependencies installed as mentioned above.

	$ cd gravityApp/app
	$ sudo python GravityServer.py

### Running with Forever

[Forever](https://www.npmjs.com/package/forever)

Forever is a tool you can use to run multiple scripts. You can install forever using the following command.

	$ [sudo] npm install forever -g

To run Gravity with forever:

	$ cd gravityApp/app
	$ forever start -a --uid gravityweb -c python GravityServer.py

If you are starting the server with nginx, you will need to disable SSL because it will be handled
by nginx.

	$ cd gravityApp/app
	$ forever start -a --uid gravityweb -c python GravityServer.py --disable
