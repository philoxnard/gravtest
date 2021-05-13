
SSL Key Generation and Configuration
--------------------------------------

[SSL Key file Resource](https://serverfault.com/questions/9708/what-is-a-pem-file-and-how-does-it-differ-from-other-openssl-generated-key-file)

### Create Server pem files.

	$ openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes

The server.pem file that was generated in the command above contains both the private key and the certificate
that the server uses for the HTTPS connection.  The beginning of the file contains the private wrapped in the tags
"-----BEGIN PRIVATE KEY-----" and "-----END PRIVATE KEY-----".

The certificate is followed wrapped in tags "-----BEGIN CERTIFICATE-----" and "-----END CERTIFICATE-----".

Note that you could specify two separate files, one for the private key and one for the certificate if you give different
filenames to the -keyout and -out arguments.  However, the TM1Server currently requires that both the private key and the certificate
be located in the PEM file.

#### Find Certificate Expiration Time

When the server starts, it uses this information to encrypt communication between the browser and the server.  Please
note that the command above indicated that the certificate is valid for 365 days.  You can determine the expiration date
of a certificate using the following command.

	$ openssl x509 -enddate -noout -in server.pem

### Generate public key from the private key

The private key contains the public key. In order to generate a file for the public key, the permissions on the private key must be correct, 600.

	$ chmod 600 server.pem
	$ ssh-keygen -y -f server.pem > server.pub

### Use Makefile to genereate key

To make the key generation easier, you can use the command in the Makefile.

	$ make generate-key