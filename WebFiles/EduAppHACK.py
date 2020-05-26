import socketserver
import threading

BUFFSIZE = 5120*1024*2



class Handler_TCPServer(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        print("Connection")
        data = self.request.recv(BUFFSIZE)
        data = data.decode("utf-8")
        print(data)
        F = open("cmd.txt", "r")
        command = F.readline()
        F.close()
        if(data == "CMD"):
            self.request.sendall(bytes(command, encoding="utf8"))
        data = self.request.recv(BUFFSIZE)
        data = data.decode("utf-8")
        print("GOT : " + str(data))
        print(str(self.request.getpeername()))





if __name__ == "__main__":
    HOST, PORT = "", 7557
    # Init the TCP server object, bind it to the localhost on 9999 port
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    # Activate the TCP server.
    # To abort the TCP server, press Ctrl-C.
    tcp_server.serve_forever()
