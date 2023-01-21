import socket
import pickle
import threading
import time

from client import socketClient

def recibir():
    while True:
        data = s.receive()
        if not data:
            continue
        print(data)

def printPost(data, socket_):
    print('-> ', data['post'])

s = socketClient('localhost', 8080)
s.connect()

r = threading.Thread(target=recibir, daemon=True)
r.start()

s.addFunction('post', printPost)

while True:
    post = input('ingrese un mensaje: ')
    s.do({'func':'mensaje', 'data':{'post':post}})
    time.sleep(0.2)

s.close()