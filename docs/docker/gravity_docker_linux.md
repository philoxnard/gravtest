
Gravity Docker Documentation for Debian Linux
=============================================

### Install Docker

[Install Docker on Debian OS](https://docs.docker.com/install/linux/docker-ce/debian/)

To run gravity as a docker image, you must have Docker installed on your host operating system.  When running gravity with Docker, all of the dependencies are built into the image itself, this way you don't have to install the python dependencies individiually on the host operating system.

Use the above instructions to install Docker on your host OS, then you can install docker-compose below which allows the gravity system to deployed much easier.

### Install Docker Compose

	$ sudo apt-get -y install python-pip
	$ sudo pip install docker-compose

### Use Docker under non-root user

	$ sudo usermod -aG docker your-user