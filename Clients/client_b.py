import socket
import threading
from queue import Queue
import pickle
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
host = "192.168.31.140"
port = 9993


def create_socket():
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(5)

    while True:
        try:
            conn, address = s.accept()
            print("Connection has been established :" + address[0] + " " + str(address[1]))
            file_name = str(conn.recv(2048), "utf-8")
            print("The peer wants : " + file_name)
            f = open(file_name, 'rb')
            l = f.read(1024)
            while l:
                conn.send(l)
                print('Sent ', repr(l))
                l = f.read(1024)
            f.close()
            print('Done sending')
            conn.close()

        except Exception as e:
            print(e)


def start_turtle():
    while True:
        cmd = input('Input ')
        if cmd == 'list':
            list_connections()
        elif 'select' in cmd:
            s1 = socket.socket()
            s1.bind(("192.168.31.140", 9994))
            s1.connect(("192.168.31.140", 9999))
            s1.send(str.encode("file.txt"))
            file_name = 'new.txt'
            with open(file_name, 'wb') as f:
                print('file opened')
                while True:
                    print('receiving data...')
                    data = s1.recv(1024)
                    print('data=%s', data)
                    if not data:
                        break
                    # write data to a file
                    f.write(data)

            f.close()
            print('Successfully get the file')
            s1.close()
        else:
            print("Command not recognized")


def list_connections():
    sock = socket.socket()
    ip = "192.168.31.140"
    port_ = 9989
    sock.bind((ip, port_))
    tracker_ip = "192.168.31.140"
    tracker_port = 9997
    sock.connect((tracker_ip, tracker_port))
    sock.send(str.encode("List", "utf-8"))
    #list_ = str(sock.recv(1024), "utf-8")
    data = sock.recv(1024)
    list_ = pickle.loads(data)
    print(list_)
    sock.close()
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()

        if x == 2:
            start_turtle()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
