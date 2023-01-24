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
    print(data)
    print('-> ', data['post'])

s = socketClient('localhost', 8080)
s.connect()

r = threading.Thread(target=recibir, daemon=True)
r.start()

s.addFunction('post', printPost)

room = input('room: ')
s.do({'func':'join', 'data':{'room':room, 'id': s.id}})
time.sleep(.5)

while True:
    post = input('mensaje: ')
    if post == '0':
        break
    s.do({'func':'sendToRoom', 'data':{'room':room, 'id': s.id, 'data':{'func': 'post', 'data': {'post': post}}}})
    time.sleep(0.2)

room = input('room: ')
s.do({'func':'leave', 'data':{'room':room, 'id': s.id}})
time.sleep(.5)

s.socket_.close()