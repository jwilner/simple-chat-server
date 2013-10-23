
# A chat server implementing select
import random, select, socket, sys, re

PORT = random.randint(6000,8000)
MAX_LISTEN = 10
MSG_SIZE = 1024

if len(sys.argv) == 1 or sys.argv[1] == 'server':
    server = socket.socket()
    server.bind(('',PORT))
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.listen(MAX_LISTEN)
    inputs = [server]
    clients = []
    pre_clients = []
    names = {}

    print( '''Starting a server. Tell folks to connect with 
        'python simple-chat-system.py -ip {0} -p {1}' '''
        .format(socket.gethostbyname(socket.gethostname()),PORT))

    try:
        while True:
            input_rdy, output_rdy, err_rdy = select.select(inputs +
                    pre_clients + clients, [], [])
            for s in input_rdy:
                if s == server:
                    client,address = server.accept()
                    pre_clients.append(client)
                    client.send('Please provide your name.')
                    print 'Connected with {0!s}.'.format(client.getsockname())
                elif s in pre_clients: 
                    data = s.recv(MSG_SIZE)
                    if data: 
                        names[s.getsockname()] = data
                        s.send("Welcome to da chat serva, {0!s}. The maximum "+
                                "message length is {1!s}. Currently, there are "+
                                "{2!s} other people in the chat: {3}."
                                .format(data,MSG_SIZE,len(clients),
                                    ', '.join(names[c.getsockname()] for c in clients)))
                        clients.append(s)
                        print 'Added {0} to the clients list.'.format(data)
                        for client in clients:
                            client.send('Everyone, please welcome {0}!'.format(data))
                        print 'Sent welcome message for {0}'.format(data)
                    pre_clients.remove(s) # this removes from pre_clients whether the person joined or not
                else:
                    data = s.recv(MSG_SIZE)
                    name = names[s.getsockname()]
                    print 'Received data {0!r} from {1}'.format(data,name)
                    if not data or data.lower() == 'let me leave':
                        for c in clients:
                            c.send('{0} has left the chat. Such a pity.'.format(name))
                        s.close()
                        clients.remove(s)
                        print 'Removed {0} from clients.'.format(name)
                    else:
                        msg = '{0}: {1}'.format(name,data.replace('\n',''))
                        for c in clients:
                            c.send(msg)
                        print 'relaying message from {0}'.format(name)
    except KeyboardInterrupt:
        print 'Server shutting down...'
        for c in clients:
            c.close()
        server.close()

elif sys.argv[1] == '-ip' and re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',sys.argv[2]) and sys.argv[3] == '-p' and sys.argv[4].isdigit():
    #client side
    try:
        s = socket.socket()
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((sys.argv[2],int(sys.argv[4])))
    except socket.error:
        print 'There was a problem connecting to the server.'
    else:
        print s.recv(MSG_SIZE)
        try:
            while True:
                inputs,o,e = select.select([s,sys.stdin],[],[s])
                for i in inputs:
                    if i is s:
                        msg = i.recv(MSG_SIZE)
                        if msg:
                            print msg
                    else:
                        msg = i.readline()
                        s.sendall(msg)
                if e:
                    print 'Connection closed.' 
                    e[0].close()
                    break
        except KeyboardInterrupt:
            s.close()
            print 'Leaving chat.'
            
