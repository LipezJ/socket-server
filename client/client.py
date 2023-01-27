import socket
import pickle
import threading
import select
import time

class socketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.functions = {}
        self.socket_ = None
        self.id = None
        self.rooms = []

    def connect(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.socket_.connect((self.host, self.port))
        self._connected()
        print(self.id)

    def _connected(self):
        data = pickle.loads(self.socket_.recv(1024))
        self.id = data['id']

    def do(self, func: str, data):
        if self.id != None:
            data['id'] = self.id
        if data is not None:
            self.socket_.send(pickle.dumps({'func': func, 'data': data}))

    def roomDo(self, room, func, data):
        if func == 'leave' or func == 'leaveAll':
            data_ = {'room': room, 'id': self.id}
            self.socket_.send(pickle.dumps({'func': func, 'data': data_}))
        if data is not None and room in self.rooms:
            data_ = {'func':'sendToRoom', 'data':{'room': room, 'id': self.rooms, 'data':{'data':data, 'func':func}}}
            self.socket_.send(pickle.dumps(data_))
    
    def userDo(self, to, func, data):
        if data is not None:
            data_ = {'func': 'sendTo', 'data': {'idSender':to, 'data':{'data':data, 'func':func}}}
            self.socket_.send(pickle.dumps(data_))

    def receive(self):
        data = pickle.loads(self.socket_.recv(1024))
        if not data:
            return 
        elif 'func' in data:
            self.functions[data['func']](data['data'], self.socket_)
            return
        return data

    def addFunction(self, name: str, func):
        if name not in self.functions and func:
            self.functions[name] = func

    def join(self, room):
        self.socket_.send(pickle.dumps({'func':'join', 'data':{'room': room, 'id': self.id}}))
        self.rooms.append(room)