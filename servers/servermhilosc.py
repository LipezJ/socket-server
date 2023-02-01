import socket
import pickle
import select
import time
import threading

from servers.socketDict import socketDict
from servers.server import socketServer

class serverMultiHilosCiclos(socketServer):
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sockets = socketDict()
        self.server = None
        self.cont = 0
        self.rooms = {}
        self.functions = {'join': self.join, 'leaveAll': self.leaveAll, 'leave': self.leave, 'sendToRoom': self.sendToRoom, 'sendTo': self.sendTo}

    #handle sockets
    def _handleSocket(self, socket, id, group):
        print(group,len(self.sockets.bySocket))
        while True:
            if group == len(self.sockets.bySocket):
                print('se elimina un hilo')
                break
            list_ = [i for i in self.sockets.bySocket.values()][group:len(self.sockets.bySocket)]
            ready_rsockets, ready_wsockets, err = select.select(list_, list_, [])
            if len(ready_rsockets) > 0:
                for socket in ready_rsockets:
                    try:
                        data = socket.recv(1024)
                    except ConnectionResetError:
                        print(id, 'desconectado')
                        try:
                            self.sockets.remove(socket)
                            self.leaveAll({'id': self.sockets.byId[socket]}, client)
                        except:
                            break
                        self.cont -= 1
                        break
                    else:
                        data = pickle.loads(data)
                        if 'func' in data:
                            self.functions[data['func']](data['data'], socket)
            time.sleep(0.1)
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(120)
        while True:
            client, address = self.server.accept()
            host, id = address
            self.sockets.add(str(id), client)
            client.send(pickle.dumps({'id': str(id)}))
            print(address, 'conectado')
            if self.cont%4 == 0:
                print('se crea un nuevo hilo')
                thread = threading.Thread(target=self._handleSocket, args=(client, id, self.cont), daemon=True)
                thread.start()
            self.cont += 1