import socket

class Connection:
    """ socket connection wrapper to connect to twitch
        irc and eventsub

    """

    BUFF_SIZE = 1024


    def __init__(self, addr):
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False     


    def connect(self):
        self.sock.connect(self.addr)
        self.connected = True


    def send(self, msg):
        data = bytes(msg + "\n", 'ASCII')

        self.sock.send(data)


    def receive(self, buffer='') -> str:
        msg = self.sock.recv(self.BUFF_SIZE)
        buffer += msg.decode('UTF-8')
        if len(msg) == self.BUFF_SIZE:
            return self.receive(buffer)
            
        return buffer


    def pong(self, data):
        msg = f'PONG {data}'
        self.send(msg)


