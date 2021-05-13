
Gravity Web Server and Framework
================================

Copyright 2019 Creative Collisions Technology, LLC
Written by: J. Patrick Farrell

The Gravity Web Framework is an open source project that brings the world together, hence the name "gravity".

This is a pure python implementation of a web server.  This is an opensource framework that provides a baseline implementation with core features such as user-login, JSON Web Tokens, and a JSON API.

You can run this web server on your host operating system with just python, but it is also possible to run this web server as a docker container. When running as a docker container, this makes the entire system much easier to manage and deploy across differerent machines and environments.

Working on Gravity? [Join the conversation](https://gravityserver.slack.com).

Documentation Examples
----------------------

While not yet complete, the goal for this documentation is to be an extremely complete and evolving documentation framework to build, develop, and deploy The Gravity Framework in multiple types of environments.  This is going to require a large effort to make sure we develop this documentation in a way that is easy to understand and complete.

[Documentation Example](http://www.davidketcheson.info/2015/05/13/add_a_readme.html)

Developers for Humanity Agreement
---------------------------------

This project is an open source project, and therefore is #softwareforhumanity.  This project has strong principles to bring the world together, to educate, and to build a baseline web framework for the world to work together.  Please read the developers documentation before you begin contributing to gravity.

This documentation describes the basic principles behind how we work together, how we structure and develop the code, and how we can support the community.

[Developers For Humanity](docs/gravity/developersforhumanity.md)

Build Dependencies
------------------

Gravity is a very versatile framework, capabile of running on Linux, MacOS and eventually Windows.  We all support running with a standard python environment, or from within a Docker container.  Follow the initial setup instructions
to get started installing the build dependencies based on your host OS and your deployment environment (python or Docker).

[Initial Setup](docs/gravity_initial_setup.md)

Build Procedure
---------------

[Python Build](docs/python/gravity_python.md)
[Docker Build](docs/docker/gravity_docker.md)

There are a couple ways to build and run this project.

1) You can run it with the python interpreter directly without compiling.
2) You can compile the program into .pyc files and run them with the python interpreter.  This will require all of the necessary .pyc files for all of the classes to run.
3) You can compile the program with pyinstaller into a single binary that you can distribute.
4) You can build the program into a docker image and run with Docker.

Run Procedure
-------------

### Run with python interpreter directly.

When you run with the python interpreter directly, there is no build or compile necessary.  However, your host machine must have all of the python dependencies installed as mentioned above.

	$ cd gravityApp/app
	$ python GravityServer.py

### Docker Run Instructions

For instructions on how to run with Docker, follow the instructions within the Gravity Docker file.

[Gravity Docker](docs/docker/gravity_docker.md)

Installing and Running in Production
------------------------------------

[Gravity Installation](docs/gravity/installation.md)

When installing for production, all the configuration and run files are located in /usr/local/gravity.

When we are running the Gravity system in production, we should be using an Nginx Front-End. We have designed the cct_nginx docker image to be run as this front-end web server.  Nginx handles multiple domains on a single server and is also necessary to be a robust web server that is necessary on the global interet.

Production is designed to run with docker. This is why the docker image only exposes the HTTPS port, port 80 internally. This means that in production, the Nginx front-end handles all of the SSL configuration and certificates.  Then is passes traffic locally to another port that gravity is configure to run on. By default we have configured the gravity-compose.yml to use port 3001, but you can change this port if desired. Ensure that your server does not expose this port to the outside world.

You can find more information about configuring and running the Ngninx Front End web server in the documentation folder.
