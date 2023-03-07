import socket
import pickle
import select
import time
import threading

from servers.server import socketServer

class serverMultiHilos(socketServer):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = {}
        self.server = None
        self.rooms = {}
        self.functions = {'join': self.join, 'leaveAll': self.leaveAll, 'leave': self.leave, 'sendToRoom': self.sendToRoom, 'sendTo': self.sendTo}

    #handle sockets
    def _handleSocket(self, socket, id: str):
        while True:
            try:
                data = socket.recv(1024)
            except ConnectionResetError:
                print(id, 'desconectado')
                del self.sockets[id]
                self.leaveAll({'id': id}, socket)
                break
            else:
                if data:
                    data = pickle.loads(data)
                    if 'func' in data:
                        self.functions[data['func']](data['data'], socket)

    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(120)
        while True:
            client, address = self.server.accept()
            host, id = address
            self.sockets[str(id)] = client
            client.send(pickle.dumps({'id': str(id)}))
            print(address, 'conectado')
            thread = threading.Thread(target=self._handleSocket, args=(client, str(id)), daemon=True)
            thread.start()
    
    #func to send
    def sendAll(self, data):
        list_ = [i for i in self.sockets.values()]
        _, ready_wsockets, err = select.select(list_, list_, [])
        for socket in ready_wsockets:
            try:
                socket.send(pickle.dumps(data))
            except:
                continue

    def sendToRoom(self, data, client):
        if len(self.rooms[data['room']]) < 2:
            return
        list_ = [self.sockets[i] for i in self.rooms[data['room']] if i != data['id'] or data['broad']]
        _, ready_wsockets, err = select.select(list_, list_, [])
        for socket in ready_wsockets:
            try:
                socket.send(pickle.dumps(data['data']))
            except:
                continue
    
    def sendTo(self, data, client):
        if data['idSender'] in self.sockets:
            self.sockets[data['idSender']].send(pickle.dumps(data['data']))
        else:
            print('este usuario no existe')