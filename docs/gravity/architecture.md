
Gravity Architecture
====================

Main Program
------------

GravityServer.py is the main program that runs the Gravity Web Server. This program can be the main entry
point into the system by running:

	$ python GravityServer.py

You also have the option though to run GravityMain.py which launches a thread where the GravityServer runs. GravityMain is currently only setup to run as an HTTP server, using this you would have an Nginx web server front-end.

The reason you would start here is that then you can launch other programs as sub-threads within the main program. It utilizes a GravityServerHelper class that you can copy and modify for a new service that you can build to run in parallel with the Gravity Server.

	$ python GravityMain.py

This is helpful when you have other services that should work along side Gravity acting as the same program. This type of architecture is mainly used when we are NOT using Docker.

If you are using Docker, ideally these other programs that are running as threads in this architecture actually would be run inside of another Docker image. Then you would use ways for the running Docker containers to communicate with each other. For more information on this you can look into the [Gravity Docker Documentation](docs/gravity_docker.md)


Adding a new view
-----------------

1. Visit the templates folder `/views` and build a new template view file (you could copy `about.j2`)
2. Visit the controller folder `/gravityApp/app/GravityControllers.py` and look to line 317 and generate a controller that fits your needs
3. In `GravityControllers.py`, visit line 31 to view the routes
4. Restart server
5. Visit `0.0.0.0/<your_additional_page>`
