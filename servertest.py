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

server.startServer()