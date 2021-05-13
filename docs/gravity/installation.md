
Gravity Installation
====================

[Nginx](../resources/nginx.md)

Gravity can be configured in many ways, but the recommended configuration is to use an Nginx Front-End web server to talk to the outside world, then within the host machine, we run the Gravity server on a local port.  The nginx web server then routes any traffic that is configured for the domain coming in on port 80 or 443 to the Gravity Server internally.

It is not recommended to run Gravity in production without the Nginx Front-end as Nginx is better suited to handle large amounts of traffic and is more robust to handle web attacks.

We have created a docker image for you that will launch the Nginx front-end, cct_nginx.  You can build this Docker image and install it so it runs on boot. This is an alternative and easier installation procedure than installing Nginx natively on the host machine.

TODO: This document will be matched with a main Gravity Makefile that will build and install the entire gravity system.

Install Directory Locations
---------------------------

In production, Gravity installs most of it's files into the Docker image itself. However, there are a few folders on the host machine that are necessary for gravity to run. These directories include

	/usr/local/gravity
	/srv/gravity

If you are configured to have multiple gravity instances for different sites, you can add sub-folders within the gravity sub-folders for each instance. It is recommended that you match the sub-folders within this directory to any domain configuration that you use to configure the nginx front-end.

If you are running on MacOS, you will need to share all of the directories from the host machine in the Docker -> Preferences... -> File Sharing.

### /usr/local/gravity

This is the directory where all program files for gravity are stored. This directory does not store dynamic data, only the program files to run gravity.

TODO: It might make more sense to have the database files or configuration files in /usr/local/gravity, but this wasn't working properly on MacOS so for now we are going to put everything data related in /srv/gravity because it seems to be working.

### /srv/gravity

This directory is for any upload files and media files that the web server should serve that are dynamic
and not included in the base image. For instance, this could include files that the user uploads, image files for user profiles, etc.

Currently configuration files for gravity are also included in this directory as of now.
