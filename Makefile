
# Top-level Makefile for the Gravity Framework and Server
# Copyright 2021 Creative Collisions Technology, LLC
# Written by: J. Patrick Farrell

IMAGE_NAME ?= docker.creativecollisionstech.com/cct/opensource/gravity

HOST_GRAVITY_DIRECTORY=/Volumes/Gravity

# Native Install
NATIVE_INSTALL_DIRECTORY=/usr/local/src/gravity
NATIVE_INSTALL_CONFIG_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/config
NATIVE_INSTALL_DATA_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/data
NATIVE_INSTALL_LOGS_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/logs
NATIVE_INSTALL_PUBLIC_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/public
NATIVE_INSTALL_VIEW_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/views
NATIVE_INSTALL_MODELS_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/models
NATIVE_INSTALL_SCHEMA_DIRECTORY=${NATIVE_INSTALL_DIRECTORY}/schema


# Location on the host machine where input and output files are placed
#  This is where files will be shared between containers.
HOST_GRAVITY_AUTH_DIRECTORY ?= ${HOST_GRAVITY_DIRECTORY}/auth
HOST_GRAVITY_DATA_DIRECTORY ?= ${HOST_GRAVITY_DIRECTORY}/data
HOST_GRAVITY_UPLOAD_DIRECTORY ?= ${HOST_GRAVITY_DIRECTORY}/data/upload
HOST_SECURITY_DIRECTORY ?= ${HOST_GRAVITY_DIRECTORY}/security

# Locations inside of the image where upload and output files are referenced
IMAGE_GRAVITY_AUTH_DIRECTORY ?= /gravity/auth
IMAGE_GRAVITY_DATA_DIRECTORY ?= /gravity/data
IMAGE_GRAVITY_UPLOAD_DIRECTORY ?= /gravity/public/upload
IMAGE_SECURITY_DIRECTORY ?= /gravity/security

# Note that we are setup to run with an Nginx front-end using Docker, therefore the HTTPS
#  server is disabled inside of the Dockerfile and we are sharing the docker images port
#  80 with another port on our host machine that nginx is setup to route the traffic to.
#  See the cct_nginx 
# If you wish to run the HTTPS server inside of the Docker image, you will have to change the Dockerfile.
# Host Configuration
HOST_HTTP_PORT ?= 3001
HOST_HTTPS_PORT ?= 443

# Image Configuration
IMAGE_HTTP_PORT ?= 80
IMAGE_HTTPS_PORT ?= 443

INITDIR=/etc/init.d

VERSION ?= version0.2.1

# **** Gravity Native installation, running and building ****

all:
	python -m compileall ./gravityApp/app

install_native:
	# This is to install Gravity natively rather than using Docker.
	# TODO: Make sure you flip the "USE_DOCKER" Configuration to False if you use this method.
	mkdir -p ${NATIVE_INSTALL_DIRECTORY}
	mkdir -p ${NATIVE_INSTALL_CONFIG_DIRECTORY}
	mkdir -p ${NATIVE_INSTALL_DATA_DIRECTORY}
	mkdir -p ${NATIVE_INSTALL_LOGS_DIRECTORY}

	cp -r gravityApp/app ${NATIVE_INSTALL_DIRECTORY}/app
	cp -r public ${NATIVE_INSTALL_DIRECTORY}/public
	cp -r views ${NATIVE_INSTALL_DIRECTORY}/views
	cp -r models ${NATIVE_INSTALL_DIRECTORY}/models
	cp -r schema ${NATIVE_INSTALL_DIRECTORY}/schema

install_native_startup_script:
	# Install the Gravity startup script, for Native installation.
	cp -p etc/init.d/gravity_native ${INITDIR}
	update-rc.d gravity_native defaults
	chmod 777 ${INITDIR}/gravity_native

# **** Gravity Native installation, running and building ****

build:
	docker build -t $(IMAGE_NAME) .

clean:
	make -C gravityApp clean
	docker rmi ${IMAGE_NAME}

install:
	# Default is to install for the Docker Configuration.
	# Note: This install is designed for Linux/Debian. Might be different for another OS.
	# The install directory where we will store all of the gravity install information.
	mkdir -p ${HOST_GRAVITY_AUTH_DIRECTORY}
	# Create the Gravity Data Directory
	mkdir -p ${HOST_GRAVITY_DATA_DIRECTORY}
	# Create the host Gravity Upload Directory
	mkdir -p ${HOST_GRAVITY_UPLOAD_DIRECTORY}
	# Create the host Gravity Security Directory
	mkdir -p ${HOST_SECURITY_DIRECTORY}
	# Copy necessary files into install directory
	cp gravity-compose.yml ${HOST_GRAVITY_DIRECTORY}/

install_startup_script:
	# Install the Gravity startup script, for Docker installation.
	cp -p etc/init.d/gravity ${INITDIR}
	update-rc.d gravity defaults
	chmod 777 ${INITDIR}/gravity

image-run:
	docker run --rm --name=gravity_server \
	-v ${HOST_GRAVITY_AUTH_DIRECTORY}:${IMAGE_GRAVITY_AUTH_DIRECTORY} \
	-v ${HOST_GRAVITY_DATA_DIRECTORY}:${IMAGE_GRAVITY_DATA_DIRECTORY} \
	-v ${HOST_GRAVITY_UPLOAD_DIRECTORY}:${IMAGE_GRAVITY_UPLOAD_DIRECTORY} \
	-v ${HOST_SECURITY_DIRECTORY}:${IMAGE_SECURITY_DIRECTORY} \
		-p ${HOST_HTTP_PORT}:${IMAGE_HTTP_PORT} \
		${IMAGE_NAME}

push:
	docker push $(IMAGE_NAME)

pull:
	docker pull $(IMAGE_NAME)

tag:
	docker tag $(IMAGE_NAME) $(IMAGE_NAME):$(VERSION)

dev:
	docker-compose -f gravity-compose.yml up

dev-d:
	docker-compose -f gravity-compose.yml up -d

generate-key:
	openssl req -new -x509 -keyout ./security/server.pem -out ./security/server.pem -days 365 -nodes
