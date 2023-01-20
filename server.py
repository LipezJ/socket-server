import socket
import pickle
import threading
import select
import time
import uuid
import re

class socketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = {}
        self.functions = {}
        self.rooms = {}
        self.server = None

    #handle sockets
    def _handleSocket(self):
        while True:
            list_ = [i['client'] for i in self.sockets.values()]
            ready_rsockets, ready_wsockets, err = select.select(list_, list_, [])
            if len(ready_rsockets) > 0:
                for socket in ready_rsockets:
                    if socket is self.server:
                        client, address = socket.accept()
                        host, id = address  
                        self.sockets[id] = {'client': client, 'id': id}
                        client.send(pickle.dumps({'id': id}))
                        print(address, 'conectado')
                    else:
                        data = socket.recv(1024)
                        if not data:
                            id = int(re.search(r'[0-9]{5}', str(socket)).group()) # provisional
                            print(id, 'desconectado')
                            self.sockets.pop(id)
                        else:
                            if socket in ready_wsockets:
                                data = pickle.loads(data)
                                if data['func']:
                                    self.functions[data['func']](data['data'], socket)
                                print('id:', data['id'])
            time.sleep(0.1)

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
    def sendAll(self, data, client):
        print(f'\n\n', self.rooms[data['name']], f'\n\n',)
        if data['name'] in self.rooms:
            for client_ in self.rooms[data['name']]:
                client_.send({data['name']: data['post']})
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.sockets['server'] = {'client': self.server, id: 'server'}
        self._handleSocket()