
SSL Implementation and Notes
============================

To keep your website secure and pass encrypted traffic between the web server and the brower, you need to be using using HTTPS with an SSL certificate.  

### Reasons to Use SSL

1) Web traffic will be encrypted between the server and the client, preventing 3rd parties from viewing your traffic.
2) Google and other search enginges down rank websites without HTTPS now and the "Not Secure" display within your browser doesn't look very professional.
3) The "Not Secure" display within your browser doesn't look professional.

Let's Encrypt
-------------

SSL certificates usually cost money.  But there is one Certificate Authority out there that you can use to get a free SSL certificate, called Let's Encrypt.

### Getting setup with Nginx on Ubuntu

[Setup Instructions](https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx)

	$ ln -s /etc/nginx/sites-available/creativecollisionstech /etc/nginx/sites-enabled/creativecollisionstech

### Debian Linux Instructions

Install certbot

	$ apt-get install certbot

If you just want to get a certificate without a specific server:

	$ sudo certbot certonly

After you run this command, you will end up with a few files in /etc/letsencrypt/live/<domain>

Obtain certificate for Nginx:

	$ sudo certbot --nginx

Renew certificate:

You need to use the email address you created the certificate with.

	$ certbot renew

Support SAN

	$ certbot certonly --webroot -w /var/www/html -d www.thegravityframework.com -d www.friendsofcrawfordpark.org -d www.mainedesigncompany.com -d www.netonos.com

Add domain to SAN list: just rerun above command with additional domain

### Let's Encrypt Certificates

It is possible to use Let's Encrypt to run create the certificate to secure the SSL connection. With Let's Encrypt, you typically end up with several files rather than the single server.pem file we need for the TM1 web application.

If you wish to take the Let's Encrypt files and creat your own server.pem file, you can contcatenate the privkey.pem file and the fullchain.pem file together to create the server.pem

	$ cd /etc/letsencrypt/live/<server name>/
	$ cat privkey.pem > server.pem
	$ cat fullchain.pem >> server.pem

#### Find Certificate Expiration Time

When the server starts, it uses this information to encrypt communication between the browser and the server.  Please
note that the command above indicated that the certificate is valid for 365 days.  You can determine the expiration date
of a certificate using the following command.

	$ openssl x509 -enddate -noout -in server.pem
