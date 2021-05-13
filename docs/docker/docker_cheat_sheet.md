
# Original Source

https://www.digitalocean.com/community/tutorials/how-to-remove-docker-images-containers-and-volumes

# List dangling images

Dangling images are layers that have no relationship to any tagged images. 

	docker images -f dangling=true

# Remove dangling images

	docker rmi $(docker images -f dangling=true -q)

# List all images

	docker images -a

# Remove all images

	$ docker rmi $(docker images -a -q)



# List all containers

	$ docker ps -a

# Remove a container

	$ docker rm ID_or_Name ID_or_Name

# List all exited containers

	$ docker ps -a -f status=exited

# Remove all exited containers

	$ docker rm $(docker ps -a -f status=exited -q)
