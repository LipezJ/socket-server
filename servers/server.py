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
    
    #general funcs
    def join(self, data, client):
        if data['room'] in self.rooms:
            self.rooms[data['room']].append(data['id'])
            print('join to', data['room'], self.rooms)
        else:
            self.rooms[data['room']] = [data['id']]
            print('create')
    
    def leaveAll(self, data, client):
        print('leave')
        try:
            for room in self.rooms:
                print(room, self.rooms[room])
                if data['id'] in self.rooms[room]:
                    if len(self.rooms[room]) < 2:
                        del self.rooms[room]
                        print('sala eliminada')
                    else:
                        self.rooms[room].remove(data['id'])
                        print(data['id'], 'ha salido de todas las rooms')
        except:
            return

    def leave(self, data, client):
        if data['id'] in self.rooms[data['room']]:
            if len(self.rooms[data['room']]) < 2:
                del self.rooms[room]
                print('sala eliminada')
            else:
                self.rooms[data['room']].remove(data['id'])
                print('ha salido de la sala', data['room'])
    
    def sendToRoom(self, data, client):
        if data['id'] in self.rooms[data['room']]:
            list_ = [self.sockets.bySocket[i] for i in self.rooms[data['room']] if (i != data['id'] or data['broad'])]
            _, ready_wsockets, err = select.select(list_, list_, [])
            for socket in ready_wsockets:
                try:
                    socket.send(pickle.dumps(data['data']))
                except:
                    continue
    
    def sendTo(self, data, client):
        if data['idSender'] in self.sockets.bySocket:
            self.sockets.bySocket[data['idSender']].send(pickle.dumps(data['data']))
        else:
            print('este usuario no existe')