import socket
import pickle
import select
import time

from socketDict import socketDict

class socketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = socketDict()
        self.functions = {}
        self.rooms = {}
        self.server = None

    #handle sockets
    def _handleSocket(self):
        while True:
            list_ = [i for i in self.sockets.bySocket.values()]
            ready_rsockets, ready_wsockets, err = select.select(list_, list_, [])
            if len(ready_rsockets) > 0:
                for socket in ready_rsockets:
                    if socket is self.server:
                        client, address = socket.accept()
                        host, id = address
                        self.sockets.add(id, client)
                        client.send(pickle.dumps({'id': id}))
                        print(address, 'conectado')
                    else:
                        try:
                            data = socket.recv(1024)
                        except ConnectionResetError:
                            print(id, 'desconectado')
                            self.sockets.remove(socket)
                            continue
                        else:
                            if socket in ready_wsockets:
                                data = pickle.loads(data)
                                if data['func']:
                                    self.functions[data['func']](data['data'], socket)
                                print('id:', data['id'])
    
    #func to send
    def sendAll(self, data):
        list_ = [i for i in self.sockets.bySocket.values()]
        _, ready_wsockets, err = select.select(list_, list_, [])
        for socket in ready_wsockets:
            try:
                socket.send(pickle.dumps(data))
            except:
                continue

    #functions to manage
    def addFunction(self, name: str, func):
        if name not in self.functions and func:
            self.functions[name] = func
    
    #rooms func
    def createRoom(self, data, client):
        if data['name'] not in self.rooms:
            self.rooms[data['name']] = []
            self.joinRoom(data, client)
            print(self.rooms)
    def joinRoom(self, data, client):
        if data['name'] in self.rooms:
            self.rooms[data['name']].append(client)
            print(self.rooms)
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.sockets.add(0, self.server)
        self._handleSocket()