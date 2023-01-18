import socket
import pickle
import threading
import select
import time
import uuid

class socketServer:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = {}
        self.functions = {}
        self.rooms = {}

    #handle funcs
    def _handleClient(self):
        while True:
            try:
                for socket_ in self.sockets:
                    self._handleSocket(self.sockets[socket_])
            except:
                continue
    def _handleSocket(self, socket_):
        client = socket_['client']
        client.settimeout(0.05)
        try:
            data = client.recv(1024)
            if not data:
                print(client, 'desconectado')
                self.sockets.pop(socket_['id'], {})
                return 0
            else:
                data = pickle.loads(data)
            try:
                if data['func'] in self.functions:
                    self.functions[data['func']](data['data'], client)
                    print(data['id'])
                elif data['room'] in self.rooms:
                    self.sendAll(data, client)
            except KeyError:
                return 0
        except socket.timeout:
            return 0

    #functions to manage
    def addFunction(self, name: str, func):
        if name not in self.functions and func:
            self.functions[name] = func
        print('functions:', self.functions)
    
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
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        clients = threading.Thread(target=self._handleClient)
        clients.start()
        while True:
            client, address = s.accept()
            if client not in self.sockets:
                uid = uuid.uuid4()
                self.sockets[uid] = {'client': client, 'room': '', 'id': uid}
                client.send(pickle.dumps({'id': uid}))