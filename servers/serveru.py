import socket
import pickle
import selectors
import threading

from servers.socketDict import socketDict
from servers.server import socketServer

class serverUnique(socketServer):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = socketDict()
        self.sel = selectors.DefaultSelector()
        self.server = None
        self.rooms = {}
        self.functions = {'join': self.join, 'leaveAll': self.leaveAll, 'leave': self.leave, 'sendToRoom': self.sendToRoom, 'sendTo': self.sendTo}

    def accept(self, sock, mask):
        conn, address = sock.accept()
        host, id = address
        self.sockets.add(str(id), conn)
        conn.send(pickle.dumps({'id': str(id)}))
        print(id, 'connected')
        conn.setblocking(False)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def read(self, conn, mask):
        try:
            data = conn.recv(1024)
            if data:
                data = pickle.loads(data)
                if data['func']:
                    self.functions[data['func']](data['data'], conn)
        except ConnectionResetError:
            self.leaveAll({'id': self.sockets.byId[conn]}, conn)
            self.sockets.remove(conn)
            self.sel.unregister(conn)
            conn.close()
            pass

    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.sel.register(self.server, selectors.EVENT_READ, self.accept)
        self.sockets.add(0, self.server)
        try:
            while True:
                events = self.sel.select() 
                for key, mask in events:
                    callback = key.data
                    callback(key.fileobj, mask)
        except KeyboardInterrupt:
            return