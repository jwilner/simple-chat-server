#chatserver3

import socket, threading

class server3(threading.Thread):
    def __init__(self,(socket,address)):
        threading.Thread.__init__(self)
        self.SOCKET = socket
        self.ADDRESS = address

    def run(self):
        print('Connected ',self.ADDRESS)
        while True:
            From = self.SOCKET.recv(1024)
            if not From:
                break
            print str(self.ADDRESS)+ ' sent '+From
            self.SOCKET.send(str(self.ADDRESS)+' sent '+From)
        self.SOCKET.close()
        print('Disconnected ',self.ADDRESS)

s = socket.socket()
s.bind(('',8889))
s.listen(4)

while True:
    server3(s.accept()).start()
