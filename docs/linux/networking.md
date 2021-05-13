
Linux Networking Resources
==========================


Restart Network Interface
-------------------------

    $ /etc/init.d/networking restart

Stop specific interface

    $ ifdown eth0

Start specific interface

    $ ifup eth0

/etc/network/interfaces
-----------------------

Everytime you change this file, make sure you restart the networking interface as shown above.

Set to DHCP:

```
auto eth0
iface eth0 inet dhcp
```