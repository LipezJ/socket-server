import pickle
import threading
import time
import psutil
import os

import servers

def mensaje(data, client):
    print(data['post'], end=' ')
    client.send(pickle.dumps({'func': 'post', 'data':{'post': data['post']}}))
    process = psutil.Process(pid=os.getpid())
    print('mem =', process.memory_info().rss / (1024 * 1024), end=' -> ')

server = servers.serverMultiHilos('localhost', 8080)
server.addFunction('mensaje', mensaje)

def sendAll():
    time.sleep(15)
    server.sendAll({'func': 'post', 'data':{'post': 'hola mundo'}})

r = threading.Thread(target=sendAll, daemon=True)
r.start()

server.startServer()