
# A chat server implementing select
import select, socket, sys, re

PORT = 8888
MAX_LISTEN = 10
MSG_SIZE = 1024

if len(sys.argv) == 1 or sys.argv[1] == 'server':
    server = socket.socket()
    server.bind(('',PORT)) 
    server.listen(MAX_LISTEN)
    inputs = [server]
    clients = []
    pre_clients = []
    names = {}

    print( '''Starting a server. Tell folks to connect with 
        'python simple-chat-system.py -ip {0!s}' '''
        .format(socket.gethostbyname(socket.gethostname())))

    try:
        while True:
            input_rdy, output_rdy, err_rdy = select.select(inputs +
                    pre_clients + clients, [], [])
            for s in input_rdy:
                if s == server:
                    client,address = server.accept()
                    pre_clients.append(client)
                    client.send('Please provide your name.')
                elif s in pre_clients: 
                    data = s.recv(MSG_SIZE)
                    if data: 
                        names[s.getsockname()] = data
                        s.send('''Welcome to da chat serva, {0!s}. The maximum message length is {1!s}. 
                                Currently, there are {2!s} other people in the chat: {3}.'''
                                .format(data,MSG_SIZE,len(clients),', '.join(names[c.getsockname()] for c in clients)))
                        for client in clients:
                            client.send('Everyone, please welcome {0!s}!'.format(data))
                        clients.append(s)
                    pre_clients.remove(s) # this removes from pre_clients whether the person joined or not
                else:
                    data = s.recv(MSG_SIZE)
                    name = names[s.getsockname()]
                    if not data or data.lower() == 'let me leave':
                        for c in clients:
                            c.send('{0} has left the chat. Such a pity.'.format(name))
                        s.close()
                        clients.remove(s)
                    else:
                        print 'relaying message from {0!s}'.format(name)
                        for c in clients:
                            c.send('{0}: '.format(name)+data)
    except KeyboardInterrupt:
        print 'Server shutting down...'
        for c in clients:
            c.close()
        server.close()

elif re.match('^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$',sys.argv[1]):
    #client side
    try:
        s = socket.socket()
        s.connect((sys.argv[1],8888))
    except socket.error as e:
        print 'There was a problem connecting to the server.'
    else:
        try:
            i,o = s,s
            while True:
                i_r, o_r, e_r = select.select([i],[o],[])
                r_i = raw_input()
                if r_i:
                    s.sendall(r_i)
                if i_r:
                    (i_r,) = i_r
                    print i_r.recv(MSG_SIZE) 
        except KeyboardInterrupt:
            s.close()
            print 'Leaving chat.'
