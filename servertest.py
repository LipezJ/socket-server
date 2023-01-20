import pickle
import threading
import time
from server import socketServer

def mensaje(data, client):
    print(data['post'], end=' -> ')
    client.send(pickle.dumps({'result':data['post']}))

server = socketServer('localhost', 8080)
server.addFunction('mensaje', mensaje)

def sendAll():
    time.sleep(15)
    server.sendAll({'post':'holamundo'})

r = threading.Thread(target=sendAll)
r.start()

server.startServer()