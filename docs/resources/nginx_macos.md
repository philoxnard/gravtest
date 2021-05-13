
Install Nginx Mac OS
--------------------

[Original Resource](https://coderwall.com/p/dgwwuq/installing-nginx-in-mac-os-x-maverick-with-homebrew)

The easiest way to install nginx on OSX is through Homebrew.  To check if homebrew is installed, just type "brew" on the command line.  If it isn't installed, check the instructions to install Homebrew.

To install nginx with homebrew:

	$ brew install nginx

Configuring Nginx
-----------------

The default place of nginx.conf on Mac after installing with brew is:

	/usr/local/etc/nginx/nginx.conf

Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

To have launchd start nginx now and restart at login:

	$ brew services start nginx

Or, if you don't want/need a background service you can just run:

	$ nginx

Running Nginx on Mac OS
-----------------------

Once nginx is installed, you will need to start the nginx daemon that runs the web server.

	$ sudo nginx

To stop nginx:

	$ sudo nginx -s stop

Test Nginx
----------

To test that the Nginx server is running, go to the following URL in a browser:

	http://localhost:8080
