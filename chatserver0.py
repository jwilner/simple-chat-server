
class server0():
    def run(self):
        print('Connected')
        while True:
            From = raw_input() #read line
            if not From:
                break
            print(From)
        print('Disconnected\n')

server0().run()
