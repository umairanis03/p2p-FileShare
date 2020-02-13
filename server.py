import socket
import pickle

s = socket.socket()
ip = "192.168.31.140"
port = 9997
s.bind((ip, port))
s.listen(5)
peers = []

a = ("192.168.31.140", 9999, "file1.txt")
b = ("192.168.31.140", 9993, "file2.txt")
peers.append(a)
peers.append(b)

while True:
    print("Tracker is Waiting for connections")
    c, address = s.accept()
    print("Tracker connected to : " + address[0] + " " + str(address[1]))
    peers.append(address)
    x = str(c.recv(1024), "utf-8")
    print("Tracker asking for list.")
    l = []
    for i in range(len(peers)):
        check_s = socket.socket()
        ip = "192.168.31.140"
        port = 9980
        s.bind((ip, port))
        s.listen(5)
        check_ip = peers[i][0]
        check_port = peers[i][1]

        try:
            check_s.connect((check_ip, check_port))
            l.append(peers[i])
        except:
            print(check_ip + " " + str(check_port) + " is offline.")

    data = pickle.dumps(l)
    c.send(data)
    c.send(str.encode("List is here:", "utf-8"))
    print("List is sent.")
    c.close()
