import threading
import time
import psutil
import os

import servers

def mem(data, client):
    process = psutil.Process(pid=os.getpid())
    print('mem =', process.memory_info().rss / (1024 * 1024), end=' -> ')
    print('hola desde el cliente')

server = servers.serverMultiHilos('localhost', 8080)
server.addFunction('mem', mem)

def sendAll():
    time.sleep(15)
    server.sendAll({'func': 'post', 'data':{'post': 'hola mundo'}})

r = threading.Thread(target=sendAll, daemon=True)
r.start()

server.startServer()