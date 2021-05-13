
Google Cloud Platform
=====================

TODO: This seciton is not complete and needs to be tested and validated.

We typically use Google Cloud Platform (CGP) to deploy the Gravity Server to the open internet.  There are many reasons for this that include usability, ease of integration, etc.  But one of the largest reasons is that GCP is carbon-neutral, meaning they are offsetting all of their carbon emissions to run their servers 100%.  Most data centers out there do not provide this guarantee and we at Creative Collisions Technology, LLC believe in sustainability in everything that we develop.

Getting Started
---------------

To get started, you will need to install the Google Cloud SDK (GCSDK).  You can find the instructions to install GCP SDK [here](https://cloud.google.com/sdk/docs/quickstart-macos).

When you download the install package from Google, it gives you the sha ID to validate that the file you download is infact the file you are looking for.  You can validate this with the following sha command.

	$ sha -a 256 filename

### Installation

As the instructions state, once you download and extract the installation file from Google, you can then install with the following command.  Make sure you extract the files to a known location that you won't be changing.

	$ cd ~/projects/google-cloud-sdk
	$ ./install.sh

Follow through all of the procedures and press "Y" for all of them except "n" for the option to send statistics to Google.

### Initialize the SDK

You should initialize the GCSDK after installation.

	$ gcloud init

### Installing Cloud SDK for Python

The preferred tooling for managing your App Engine applications in Python is Google Cloud SDK. Since this project is built with python, we should install the python app engine tool.

	$ gcloud components install app-engine-python

### Updating the Google Cloud SDK

	$ gcloud components update

### Set Zone

	$ gcloud config set compute/zone us-central1-b


### Create a three node cluster

	$ gcloud container clusters create hello-cluster --num-nodes=3

### To see the clusters three worker VM instances

	$ gcloud compute instances list

To see the Pod created by the Deployment, run the following command:

To view the external IP address:

	$ kubectl get service
	$ kubectl get pods

You can see the new replicas running on your cluster by running the following commands:

	$ kubectl get deployment hello-web

Deactivate Cloud Load Balancer

	$ kubectl delete service hello-web

Delete a Container Cluster

	$ gcloud container clusters delete hello-cluster
