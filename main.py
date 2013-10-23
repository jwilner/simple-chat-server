import socket

if __name__ == '__main__':
    PORT = 8000
    s = socket.socket()
    print 'Connecting to ', socket.gethostbyname(socket.gethostname())
    s.bind(('',PORT))
    s.listen(10)
    s.setblocking(False)
    clients = []
    i = 0
    try:
        while True:
            i += 1
            try:
                c, (ip, port) = s.accept()
            except socket.error:
                pass
            else:
                print ip, port, ' just connected!'
                c.setblocking(False)
                clients.append(c)

            for client in clients:
                try:
                    data = client.recv(1000)
                except socket.error:
                    pass
                else:
                    print 'Received message: ', data
                    for c in clients:
                        c.send(data)
    except KeyboardInterrupt:
        print 'Ran ',i,' times'
