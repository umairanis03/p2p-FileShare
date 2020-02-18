import socket
import pickle
from _socket import SOL_SOCKET, SO_REUSEADDR

# Tracker Provides list of connected peers to the requesting peer
# Create Tracker socket for listening to peers
s = socket.socket()
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
ip = "192.168.31.140"
port = 9997

# Bind the socket to the port

s.bind((ip, port))
s.listen(5)
peers = []
peers.clear()

# Append the list of peers & files possessed by them
a = ("192.168.31.140", 9999, "file.txt")
b = ("192.168.31.140", 9993, "file1.txt")
c = ("192.168.31.140", 9899, "file2.txt")
peers.append(a)
peers.append(b)
peers.append(c)
print(peers)

# Create Infinite Loop for accepting Connections from peers
while True:
    print("Tracker is Waiting for connections")
    c, address = s.accept()
    # Accept the conncetion from peer
    print("Tracker connected to : " + address[0] + " " + str(address[1]))

    x = str(c.recv(1024), "utf-8")
    print("Tracker asking for list.")
    l = []
    # for i in range(len(peers)):
    #     check_s = socket.socket()
    #     ip = "192.168.31.140"
    #     port = 9980
    #     check_s.bind((ip, port))
    #     check_s.listen(5)
    #     check_ip = peers[i][0]
    #     check_port = peers[i][1]
    #
    #     try:
    #         check_s.connect((check_ip, check_port))
    #         l.append(peers[i])
    #         check_s.close()
    #     except:
    #         print(check_ip + " " + str(check_port) + " is offline.")

    data = pickle.dumps(peers)
    # Send the list to the peer
    c.send(data)
    c.send(str.encode("List is here:", "utf-8"))
    print("List sent to the requesting peer \n")

    # Close the connection
    c.close()
