import socket
import pickle
import select
import time

from servers.socketDict import socketDict
from servers.server import socketServer

class serverCiclo(socketServer):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = socketDict()
        self.server = None
        self.rooms = {}
        self.functions = {'join': self.join, 'leaveAll': self.leaveAll, 'leave': self.leave, 'sendToRoom': self.sendToRoom, 'sendTo': self.sendTo}

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
                        self.sockets.add(str(id), client)
                        client.send(pickle.dumps({'id': str(id)}))
                        print(address, 'conectado')
                    else:
                        try:
                            data = socket.recv(1024)
                        except ConnectionResetError:
                            print(id, 'desconectado')
                            self.sockets.remove(socket)
                            self.leaveAll({'id': self.sockets.byId[socket]}, client)
                            continue
                        else:
                            if socket in ready_wsockets:
                                data = pickle.loads(data)
                                if data['func']:
                                    self.functions[data['func']](data['data'], socket)
            time.sleep(0.1)
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.sockets.add(0, self.server)
        self._handleSocket()