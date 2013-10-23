# chatserver1.py

import socket

class server1 :
    def __init__(self, (socket, address) ):
        self.SOCKET=socket
        self.ADDRESS=address

    def run(self) :
        print 'Connected ', self.ADDRESS 
        while True :
            From=self.SOCKET.recv(1024) # Read from client
            if not From : break
            self.SOCKET.send(From)
        self.SOCKET.close()
        print 'Disconnected ', self.ADDRESS

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8888))
s.listen(1)

server1( s.accept() ).run();
