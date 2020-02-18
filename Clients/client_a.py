import socket
import threading
from queue import Queue
import pickle

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
host = "192.168.31.140"
port = 9999


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


def start_shell():
    while True:
        cmd = input('list or select -->\n')
        if cmd == 'list':
            tracker()
        elif 'select' in cmd:
            s1 = socket.socket()
            s1.bind(("192.168.31.140", 9990))
            input_ip = input("Input the IP num -->")
            input_port = int(input("Input the port number -->"))
            input_file = input("Input the file name -->")
            try:
                s1.connect((input_ip, input_port))
                s1.send(str.encode(input_file))
                # Accepting Request For File
                file_name = 'new.txt'
                with open(file_name, 'wb') as f:
                    print('file opened')
                    while True:
                        print('receiving data...')
                        data = s1.recv(1024)
                        print(data)
                        if not data:
                            break
                        # write data to a file
                        f.write(data)
                f.close()
                print('Successfully get the file \n')
                s1.close()
            except Exception as e:
                print(e)
        else:
            print("Command not recognized")


def tracker():
    sock = socket.socket()
    ip = "192.168.31.140"
    port_ = 9998
    sock.bind((ip, port_))
    tracker_ip = "192.168.31.140"
    tracker_port = 9997
    sock.connect((tracker_ip, tracker_port))
    sock.send(str.encode("List", "utf-8"))
    # list_ = str(sock.recv(1024), "utf-8")
    data = sock.recv(1024)
    list_ = pickle.loads(data)
    print(list_)
    sock.close()


def create_threads():
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
            start_shell()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_threads()
create_jobs()
