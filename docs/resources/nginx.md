
Nginx
=====

Nginx is an opensource web server.  It can run on all platforms but will start with talking about OSX.

If you wish you run multiple websites with multiple instances of Gravity running at the same time, this is possible on a Linux server by using the nginx server as your front end.  When you run multiple websites using Nginx as your front end multiplexer for multiple websites, you actually will be disabling the internal HTTPS server within Gravity and using Nginx to handle the SSL.

Install Nginx Linux
-------------------

[Resource](https://linuxize.com/post/how-to-install-nginx-on-ubuntu-18-04/)

	$ sudo apt update
	$ sudo apt install nginx

Once the installation is completed, Nginx service will start automatically. You can check the status of the service with the following command:

	$ sudo systemctl status nginx

Nginx Status
------------

	$ sudo systemctl status nginx

Managing Nginx Service
----------------------

You can manage the Nginx service in the same way as any other systemd service.

To stop the Nginx service, run:

	$ sudo systemctl stop nginx

To start it again, type:

	$ sudo systemctl start nginx

To restart the Nginx service:

	$ sudo systemctl restart nginx

Reload the Nginx service after you have made some configuration changes:

	$ sudo systemctl reload nginx

By default Nginx service will start on boot. If you want to disable the Nginx service to start at boot:

	$ sudo systemctl disable nginx

Use the enable option with the systemctl command to enable Nginx:

	$ sudo systemctl enable nginx

Use the disable option with the systemctl command to disable Nginx:

	$ sudo systemctl disable nginx

Configuring for a single site
-----------------------------

By default there is a configuration file that redirects all of the traffic for any host
name, including the server IP address, to /var/www/html. This is how nginx is configured by default but if we want to use it with Gravity, this isn't the way we want to have it running.

We want to re-direct all traffic coming into the web server to a local internal port, defaulted to port 3001. This will allow us run Gravity on a separate port internally to the server, and Nginx will act as the front-end web server.

There is an example configuration file in this project under etc/nginx/conf.d
With some slight modifications after you use letencrypt.org to generate an SSL certifcate file. For more information on how to generate the certicate, check this doc file [SSL Certificates](docs/resources/SSL.md)

After making some slight modifications to this file, from the root folder, use this command to copy it to the correct location.

	$ cp etc/nginx/conf.d/gravity.conf /etc/nginx/conf.d/
	$ sudo systemctl restart nginx    # Restart server after the configuration change

Configuring for multiple sites
------------------------------

By default, nginx is configured only to server a single web site.  You can configure it to
server multiple websites by following the instructions below.  The sites-available directory
contains a list of configuration files that can be used to configure nginx.

	$ ls /etc/nginx/sites-available

The config files inside of sites-available are not enabled until you link them to the sites-enabled
directory. These config files follow the same format as the configuration file for the single site, but they are configured for a particular domain name and can redirect to different internal ports.

	$ ln -s /etc/nginx/sites-available/<config_file> /etc/nginx/sites-enabled/<config_file>

On install, there should be a file /etc/nginx/sites-available/default that you can use to as a baseline.  However, Gravity also has a sample file in this project in etc/nginx/sites-available/thegravityframework that you can use.

Use the Example, where "thegravityframework" is the config file.

	$ cp etc/nginx/sites-available/thegravityframework /etc/nginx/sites-enabled/
	$ ln -s /etc/nginx/sites-available/thegravityframework /etc/nginx/sites-enabled/thegravityframework
	$ sudo systemctl restart nginx    # Restart server after the configuration change

CORS
====

[Nginx Config](https://enable-cors.org/server_nginx.html)

[CORS Protocol](https://fetch.spec.whatwg.org/#cors-protocol)

Logs
====

	$ cat /var/log/nginx/access.log
	$ cat /var/log/nginx/error.log







