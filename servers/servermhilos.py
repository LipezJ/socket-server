import socket
import pickle
import select
import time
import threading

from socketDict import socketDict
from servers.server import socketServer

class serverMultiHilos(socketServer):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = {}
        self.functions = {}
        self.rooms = {}
        self.server = None

    #handle sockets
    def _handleSocket(self, socket, id):
        while True:
            try:
                data = socket.recv(1024)
            except ConnectionResetError:
                print(id, 'desconectado')
                del self.sockets[id]
                break
            else:
                if data:
                    data = pickle.loads(data)
                    if 'func' in data:
                        self.functions[data['func']](data['data'], socket)
                    print('id:', data['id'])
    
    #func to send
    def sendAll(self, data):
        list_ = [i for i in self.sockets.values()]
        _, ready_wsockets, err = select.select(list_, list_, [])
        for socket in ready_wsockets:
            try:
                socket.send(pickle.dumps(data))
            except:
                continue
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(120)
        while True:
            client, address = self.server.accept()
            host, id = address
            self.sockets[id] = client
            client.send(pickle.dumps({'id': id}))
            print(address, 'conectado')
            thread = threading.Thread(target=self._handleSocket, args=(client, id), daemon=True)
            thread.start()