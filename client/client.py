import socket
import pickle
import threading

class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.functions = {}
        self.socket_ = None
        self.id = None
        self.rooms = []

    def connect(self, const: bool=True):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.socket_.connect((self.host, self.port))
        self._connected(const)
        print(self.id)

    def _connected(self, const):
        data = pickle.loads(self.socket_.recv(1024))
        self.id = data['id']
        if const:
            receivingThread = threading.Thread(target=self._receiving, daemon=True)
            receivingThread.start()

    def do(self, func: str, data={}):
        if self.id != None:
            data['id'] = self.id
        if data is not None:
            self.socket_.send(pickle.dumps({'func': func, 'data': data}))

    def roomDo(self, func: str,  room='', data={}, broad: bool=True):
        if func == 'leave' or func == 'leaveAll':
            data_ = {'room': room, 'id': self.id}
            self.socket_.send(pickle.dumps({'func': func, 'data': data_}))
        if data is not None and room in self.rooms:
            data_ = {'func':'sendToRoom', 'data':{'room': room, 'broad': not broad, 'data':{'data':data, 'func':func}}}
            if broad:
                data_['data']['id'] = self.id
            self.socket_.send(pickle.dumps(data_))
    
    def userDo(self, func: str, to: str, data={}):
        if data is not None:
            data_ = {'func': 'sendTo', 'id': self.id, 'data': {'idSender':to, 'data':{'data':data, 'func':func}}}
            self.socket_.send(pickle.dumps(data_))

    def receive(self):
        data = pickle.loads(self.socket_.recv(1024))
        if not data:
            return 
        elif 'func' in data:
            self.functions[data['func']](data['data'], self.socket_)
            return
        return data

    def _receiving(self):
        while True:
            data = self.receive()
            if not data:
                continue

    def addFunction(self, name: str, func):
        if name not in self.functions and func:
            self.functions[name] = func

    def join(self, room: str):
        self.socket_.send(pickle.dumps({'func':'join', 'data':{'room': room, 'id': self.id}}))
        self.rooms.append(room)
    
    def close(self):
        self.socket_.close()