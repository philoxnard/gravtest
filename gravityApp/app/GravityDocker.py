#!/usr/bin/env python

"""
GravityDocker.py

Docker API class.

Copyright 2019
Written by: J. Patrick Farrell

python docker-compose documentation: https://docker-py.readthedocs.io/en/stable/index.html

"""

import docker
import threading

class GravityDocker():

	def __init__(self):

		self.client = docker.from_env()

	def pruneContainers(self):
		"""
		This function deletes Delete stopped containers.

		This does the same as: docker container prune -f
		"""

		try:
			result = self.client.containers.prune()

			if 'SpaceReclaimed' in result:
				print("Space reclaimed from Containers = %s" % result["SpaceReclaimed"])

			return True
		except docker.errors.APIError as e:
			print(e)
			return False

	def pruneImages(self):
		"""
		This function deletes ununsed images.
		"""

		try:
			result = self.client.images.prune()

			if 'SpaceReclaimed' in result:
				print("Space reclaimed from Images = %s" % result["SpaceReclaimed"])

			return True
		except docker.errors.APIError as e:
			print(e)
			return False

	def printRunningContainerNames(self):

		container_list = self.client.containers.list()

		for container in container_list:
			print("Image Name: %s, Container Name: %s" % ( container.attrs['Config']['Image'], container.name ))

	def isContainerRunning(self, containerName):

		container_list = self.client.containers.list()

		for container in container_list:
			if container.name == containerName:
				return True

		return False

	def getContainer(self, containerName):

		container_list = self.client.containers.list()

		for container in container_list:
			if container.attrs['Config']['Image'] == containerName:
				return container

	def runCommandInContainer(self, containerName, command):
		"""
		This runs from a image that is not running, so it will start a new container.

		If you pass detach=True into the run function, then it will create a new detacked tontainer.
		"""

		self.client.containers.run( containerName, command )

	def run(self, imageName, command, volumes=None):
		"""
		This functions runs the command in a new docker container based on the image

		For volumes, the key is the host path, bind is the volumne inside of the container.
		"""

		# Note: if you set "detach" to equal true, it will detach from this thread and you will be returned a
		#  container rather than the std out and error.
		try:
			std_out = self.client.containers.run( imageName, command, volumes=volumes, detach=False, remove=True )
		except docker.errors.ContainerError:
			reason =  "There was an exception running the container"
			return False, reason
		except docker.errors.ImageNotFound:
			reason = "Docker image %s was not found" % imageName
			return False, reason
		except docker.errors.APIError:
			reason = "There was a docker API error"
			return False, reason

		return True, std_out


	def runCommandInRunningContainer(self, containerName, command):
		"""
		This function is for a running container. It is expected here that the container is already running.

		"""

		container = self.getContainer( containerName )

		if container != None:
			result = container.exec_run( command )
		else:
			result = "There is no running container for %s" % containerName
			print(result)
			return 1, result

		# Return the return code and standard output
		return result.exit_code, result.output

	def runCommandInThread(self, containerName, command):

		t = threading.Thread( target=self.runCommandInRunningContainer, args=(containerName, command) )
		t.daemon = True
		t.start()


if __name__ == '__main__':

	gravity_docker = GravityDocker()

	result = gravity_docker.pruneContainers()
	result = gravity_docker.pruneImages()
