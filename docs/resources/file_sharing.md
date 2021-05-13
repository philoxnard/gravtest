
File Sharing
============

This file contains information about sharing files and folder across a network.


Installl

apt-get install smbclient

smbclient -L //

// tells it that it is a cifs mount.

mount //pmac.lan /mnt/

Set mount options.

You must enable windows file Sharing for a specific account, which is under the advanced options.


To actually mount the directory:

    $ mount -t cifs //pmac.lan/<folder name> /mnt/<point> -o username=<username>



Linux Tools
-----------

You will need a linux client to connect to an SMB server:

    sudo apt-get update
    sudo apt-get install cifs-utils



nfs always works
can be easier to debug.


Mac Get Active ID

    id -un



