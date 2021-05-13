
TCP/IP Capture and Replay Notes
===============================

You can use wireshark to capture pcap files that contain network information.


Replay
------

You can use the program tcpreplay to play a pcap file.

Install on Mac OS.

    $ brew install tcpreplay


tcpreplay -i eth7 -tK --loop 5000 --unique-ip smallFlows.pcap