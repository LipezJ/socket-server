import socket
import pickle
import select

class socketServer:
    #functions to manage
    def addFunction(self, name: str, func):
        if name not in self.functions and func:
            self.functions[name] = func
    
    def sendAll(self, data):
        list_ = [i for i in self.sockets.bySocket.values()]
        _, ready_wsockets, err = select.select(list_, list_, [])
        for socket in ready_wsockets:
            try:
                socket.send(pickle.dumps(data))
            except:
                continue