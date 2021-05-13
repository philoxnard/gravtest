
Gravity Docker Instructions for Mac OS
======================================

On Mac OS, you should download Docker Desktop to your computer

[Docker Desktop](https://www.docker.com/products/docker-desktop)

## MacOS Installation Instructions

1. Install Pyton dependencies
	`$ pip install bcrypt Jinja2 PyJWT passlib`

2. Install Docker
	- Complete Docker Sign up process. This will require email verification. Remember your ID and password.
	- [Install Docker on MacOS](https://docs.docker.com/docker-for-mac/install/)
	- Double click Docker.dmg
	- Move the Docker icon to your application folder
	- Open Docker application (You will see _We are whaly happy to have you._ upon completion)
	- Sign in using the ID and password from earlier
	- To check that you have docker installed type `docker -v` into your terminal

3. Install Docker Compose (two commands in terminal application)
	- `sudo apt-get -y install python-pip`
	-	`sudo pip install docker-compose`

4. Homebrew Python Installation Process
	- `brew install python`
	- `easy_install pip`
	- `pip install --upgrade pip`
	- `sudo apt-get update`
	- `pip install docker-compose`