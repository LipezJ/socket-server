import socket
import pickle
import threading
import select
import time
import uuid

class socketClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.functions = {}
        self.socket_ = None
        self.id = None

    def connect(self):
        self.socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        self.socket_.connect((self.host, self.port))
        self._connected({})
        print(self.id)
        
    def _connected(self, data):
        self.socket_.send(pickle.dumps(data))
        data = pickle.loads(self.socket_.recv(1024))
        self.id = data['id']

    def do(self, data):
        if self.id != None:
            data['id'] = self.id
        if 'func' in data and 'data' in data:
            self.socket_.send(pickle.dumps(data))
    def receive(self):
        return pickle.loads(self.socket_.recv(1024))