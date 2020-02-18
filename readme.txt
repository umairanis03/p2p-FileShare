1. Contains a tracker ( server.py)

The work of the tracker is find the request from the peers, and provide them list of peers on the network.
Tracker also provides file name.
The list is static, tracker does not regularly checks if the peer is online or not, if the peer is offline, then while asking for a file will throw an errot.


2. Peers ( client_c.py, client_a.py, client_b.py)

The system contains three clients, with same ip but different ports. This is client side script which will be used to send and ask for files from fellow peers.


Procedure to run:
1. Run server.py
2. Run any two or three clients
3. On client shell there, it will ask for an input, 'list' is for requesting peer and file list from tracker, 'select' will guide you through requesting file
4. 'list' will give you list of peers, their ip, port numbers, file they have
5. If you go with 'select'
 --> Input IP address from list
 --> Input port number from list
 --> Input file name from list
 --> File will be stored in 'new.txt'

Requirements:

python >=3.x
import pickle
import threading
import socket
import queue

More than two sockets are combined will multi-threading for achieving this task. One threads runs infinitely to accept file requests from peers.
Another thread is given two shell.

Note : server.py & client_c.py are properly connected for understanding