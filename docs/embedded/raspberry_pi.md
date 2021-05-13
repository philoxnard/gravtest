
Gravity on the Raspberry PI
===========================

Gravity was designed first to run an embedded system.  Most web frameworks out there start with the assumption that they will be running in the cloud. The Gravity Server starts by using a embedded system methodology so that I can run the server on a local machine without access to the internet.

One of the most widely used embedded systems is a raspberry pi. A raspberry pi is a cheap $40 computer you can purchase out the Internet that will allow you to run a Linux operating system.

Gravity was designed to run on the a raspberry pi system so that you can bring up your own web interface and control the system from the local area network.

Installing Gravity on a Raspberry PI
------------------------------------

[Raspberry PI Raspian Image Download](https://www.raspberrypi.org/downloads/raspbian/)

To install gravity on a raspberry pi must first create a raspberry pi image that you can download from the Internet. Once you create that image then you can download the source code on the raspberry high and have the operating system load Gravity on Boot.

### Create a Raspian SD Card

The first step to getting a raspberry PI system running with Gravity is to downoad the operating system image and load it onto an SD card. It is recommended that you use at least a 32 GB SD Card.

- Ensure you have a 32GB nano sized SD card
- Connect your SD card to your computer using a slide in sim card or some other card reader
- Download the [Raspian image](https://www.raspberrypi.org/downloads/raspbian/)
  - _Raspbian Buster with desktop and recommended software_
- [Flash it onto the SD card](https://studio.youtube.com/video/hNaWS2UYXWk/edit)
  - Download [balenaEtcher](https://www.balena.io/etcher/) and install it
  - Use balenaEtcher to flash the Raspian image you downloaded above to your SD card
- [Connect a USB keyboard and a USB mouse and get it up and running](https://studio.youtube.com/video/Ievd4u6KFI0/edit)

Rather that repeating the instructions from the Raspberry PI documentation, you should follow the instructions on the website above.

### Loading Gravity into the Raspian Image

Once you have loaded the Raspian image, you should plug it into a keyboard, mouse and monitor and boot the board.  When it loads, you will get a screen that looks like a normal desktop.  In the top left corner, there is a button you can use to open a Terminal window.

From here, you should follow the instructions inside of the Gravity Python Documentation to download the code.  However there are some special steps here you should follow to install Gravity so it loads on boot.

#### Installing Gravity to Load on Boot

TODO
