import pickle
from server import socketServer

def mensaje(data, client):
    print(data['post'], end=' -> ')
    client.send(pickle.dumps({'result':data['post']}))

server = socketServer('localhost', 8080)

server.addFunction('mensaje', mensaje)

server.startServer()