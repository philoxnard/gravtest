# Use an official Python runtime as a base image
FROM docker.creativecollisionstech.com/cct/cct_base_python

MAINTAINER Patrick Farrell <patrick@creativecollisionstech.com>
LABEL Description="Gravity Web Server" Vendor="creativecollisionstech" Version="0.2.1"

# Make port 80 available to the world outside this container
EXPOSE 80

# If you are using the HTTPS server, make port 443 available to the world outside this container
# Note this is not enabled by default because we are using an Nginx front-end web server.
#EXPOSE 443

# Set the working directory
WORKDIR /

# Make the gravity directory. This directory is shared from the host typically.
RUN mkdir -p /gravity

# Create the data directory, this will be shared from the host machine.
RUN mkdir -p /gravity/data

# Copy the current directory contents into the container at /app
ADD ./gravityApp/app /app

# Add the HTML directory to the image
ADD ./public /gravity/public

# Add the templates directory to the image
ADD ./views /gravity/views

# Add the templates directory to the image
ADD ./models /gravity/models

# Add the schema directory
ADD ./schema /gravity/schema

# Add the .env file
ADD ./.env /

# Run app.py when the container launches, currently disables HTTPS Server
#  because we are configured to run with an Nginx Front-End, see cct_nginx
CMD ["python", "app/GravityServer.py", "--disable"]

# Use this if you want to run with the HTTPS server inside of the Docker Image
#CMD ["python", "app/GravityServer.py"]