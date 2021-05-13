
Gravity Docker Documentation
============================

These instructions explain how to get Gravity running with Docker.  This is NOT required to run Gravity, you can run Gravity with just python on your host machine.  However, for a production environment it is recommened to build and run with Docker.

Build Dependencies
------------------

[Debian Linux Instructions](docs/docker/gravity_docker_linux.md)
[Mac OS Instructions](docs/docker/gravity_docker_macos.md)

You will need to install and configure Docker on your host machine before you can build and run Gravity as a Docker container.  Use the instructions above based on the platform you are deploying on (Linux, MacOS, Window) to setup Docker.  Note Windows has not yet been tested which is why the documentation does not yet exist.

Gravity Docker Build Procedure
------------------------------

### Docker Build

Use these instructions to first build the Creative Collisions Docker base images.  You can also pull these images from the Docker registry (TODO).

The way Docker works is that you can create image layers.  The base layer is our framework layer and it contains all of the dependencies we need for our application.  We build all of the dependencies into the base image because quite often the base images need access to the internet to download the dependencies and build the image.

Once the base image is built, it is much quicker to build the gravity image because it just contains the application code and doesn't need to download dependencies from the internet for every build.

#### Docker Base Image Build

To build gravity with Docker, you must first build the base Docker image for python.  You can get this from the following Creative Collisions Gitlab repository.

[CCT Base Docker Images](https://gitlab.com/cct_opensource/cct_base)

The Creative Collisions Technology base docker images are available in another Git reposository.

	$ git clone git@gitlab.com:cct_opensource/cct_base.git

Once you clone the cct_base project, look at the README.md file within that project and use the Makefile inside of this project to build the base Docker images.

After you build the base images, you can then build the gravity Docker image as explained in the following section.

#### Docker Gravity Image Build

Clone the repository for gravity

	$ git clone git@gitlab.com:cct_opensource/gravity.git

The Makefile has been configured to build the gravity image.  If you want more information on how
to manually build the image with the docker command lines tools, please read the following sections.  The
easiest way to build the image is just to run the following command from within this folder.

	$ make build

After this command is run, you have a docker image named docker.creativecollisionstech.com/cct/opensource/gravity You can view all of your docker images using this command.

	$ docker images

### Start Gravity Server with Docker

Note that there is a configuration variable inside of the GravityConfiguration file that you will need
to set so that Docker can be run and find the appropriate template files.  Set USE_DOCKER to True.

The Makefile has been configured to start the gravity image from this directory with binded volumes
that share folders from the host machine to the image.  The easiest way to start the image is to use the following command:

	$ make image-run

### Start Gravity Server with Docker

The Makefile is configured to run the Gravity server with the included docker-compose file.

Run development version in the foreground:

	$ make dev

Run development version in the background:

	$ make dev-d


Docker Logs
-----------

This command displays all of the output the container has generated so far.

If there’s too much output for a single screen, pipe it to a buffering command like less.

	$ docker logs ContainerName/ContainerID | less

But sometimes you want to follow the logs as the container is running. There’s a command line option with an appropriate name for that: run docker logs with –-follow.

	$ docker logs --follow ContainerName/ContainerID

Show timestamps

	$ docker logs --timestamps ContainerName/ContainerID

Show logs since a particular time/date:

	$ docker logs --since 2017-05-03 ContainerName/ContainerID

To see last n lines of logs
In this case, last 2500 lines will be displayed

	$ docker logs --tail 2500 ContainerName/ContainerID

