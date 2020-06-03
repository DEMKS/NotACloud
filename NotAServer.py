import mysql.connector
import socketserver
import base64
import base64
from pathlib import Path
from os import makedirs, listdir, remove

BUFFSIZE = 5120 * 1024 * 2


def FileBase64Enc(path):
    with open(path, 'rb') as image:
        FileEnc = image.readlines()
    FileEnc = map(base64.b64encode, FileEnc)
    return FileEnc


def FileBase64Dec(s, save_path, name):
    s = map(base64.b64decode, s)
    with open(save_path + name, 'wb') as file:
        for i in s:
            file.write(i)


def FileBase64Dec2(s, save_path, name):
    s = map(base64.b64decode, s)
    with open(save_path + name, 'wb') as file:
        for i in s:
            file.write(i)


def EncodeFilename(Filename):
    Filename = str(base64.b64encode(bytes(Filename.encode("utf8"))))
    Filename = Filename[2:len(Filename) - 1]
    return Filename


def DecodeFilename(Filename):
    print(Filename)
    Filename = str(base64.urlsafe_b64decode(Filename))
    Filename = Filename[2:len(Filename) - 1]
    return Filename


class Handler_TCPServer(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)

    def handle(self):
        def ProcessLogin(data):
            print("Another data :" + data)
            Login, Rpass = data.split("|")[1], data.split("|")[2]
            print("Give me some Ls")
            if Login == '' or Rpass == '':
                print("VALYA GAY")
                return False
            DB = mysql.connector.connect(host="127.0.0.1", user="root", passwd="DonAcDum7557")
            cursor = DB.cursor()
            cursor.execute("USE userinfo")
            print("SECTOR:" + sector)
            print("LOGIN : " + Login)
            cursor.execute("SELECT password FROM users WHERE login='" + Login + "'")
            Pass = ''
            for x in cursor:
                print("X: " + str(x))
                Pass = str(x)
                Pass = Pass[2:]
                Pass = Pass[:len(Pass) - 3]
            print("DB PASS:" + Pass)
            print("Request login : " + Login)
            if Rpass == Pass:
                return True
            else:
                print("RPASS {}".format(Rpass))
                return False

        print("Connection")
        # self.request - TCP socket connected to the client
        data = self.request.recv(BUFFSIZE)
        data = data.decode("utf-8")
        print(data)
        sector, next = '', 0
        sector = data.split('|')[0]
        print("DATA : " + str(data))
        print("Next : " + str(next))
        if sector == "L":
            # There goes the login part
            if ProcessLogin(data):
                self.request.sendall("Auth succeed".encode())
            else:
                self.request.sendall("Auth error".encode())
        elif sector == "U":
            if ProcessLogin(data):
                data = data.split("|")
                print(data)
                print("DATA[1] = " + data[1])
                Login, Filename = data[1], data[3]
                print("Filename {}".format(Filename))
                Filename = EncodeFilename(Filename)
                data = data[4:]
                print("DATA = " + str(data))
                if Path("./Uploads/" + Login).is_dir():
                    # in range(4, (len(data)-1)
                    FileBase64Dec(s=data, save_path="./Uploads/" + Login + "/", name=Filename)
                else:
                    makedirs("./Uploads/" + Login)
                    print("MAKING FILE")
                    FileBase64Dec(s=data, save_path="./Uploads/" + Login + "/", name=Filename)
            else:
                self.request.sendall("Auth error".encode())
        elif sector == "C":
            if ProcessLogin(data):
                print("Good login")
                print(listdir("./Uploads/" + data.split("|")[1]))
                print("./Uploads/" + data.split("|")[1])
                string = ''
                for i in listdir("./Uploads/" + data.split("|")[1]):
                    string += DecodeFilename(str(i)) + '|'
                print("STRING : " + string)
                self.request.sendall(string.encode())
            else:
                self.request.sendall("Login is incorrect".encode())
                print("Some errors were occurred during logging in")
        elif sector == "D":
            # There goes the download part
            if ProcessLogin(data):
                print("Received file download packet : %s" % data)
                print(data.split('|'))
                data = data.split('|')
                Filename = data[len(data) - 1]
                Filename = EncodeFilename(Filename)
                if Path("./Uploads/" + data[1] + "/" + Filename.replace("/", "a")).is_file():
                    print("Filename is correct")
                    fileenc = FileBase64Enc("./Uploads/" + data[1] + "/" + Filename)
                    file = ''
                    for i in fileenc:
                        string = str(i)[:len(str(i)) - 1]
                        string = string[2:]
                        file += string + '|'
                    print("Sending this shit" + str(file))
                    self.request.sendall(bytes(("S|" + file), encoding="utf8"))
                else:
                    print("System hack attempt detected")

            else:
                self.request.sendall("Auth error".encode())
        elif sector == "R":
            # Removing file(Under development)
            if ProcessLogin(data):
                data = data.split('|')
                filename = EncodeFilename(data[3])
                print(data)
                if Path("./Uploads/" + data[1] + "/" + filename).is_file():
                    print("We are about to delete %s user's %s file" % (data[1], filename))
                    remove("./Uploads/" + data[1] + "/" + filename)
                    self.request.sendall(bytes("File deleted", encoding="utf8"))
            else:
                self.request.sendall("Auth error".encode())
        else:
            self.request.sendall("Some error occurred during tests".encode())
            print(data)


if __name__ == "__main__":
    HOST, PORT = "", 7557
    tcp_server = socketserver.TCPServer((HOST, PORT), Handler_TCPServer)
    tcp_server.serve_forever()
