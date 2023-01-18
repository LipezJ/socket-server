import socket
import pickle
import time

from client import socketClient

s = socketClient('localhost', 8080)
s.connect()

t = True
post = ' '

while len(post) > 0 or t:
    t = False
    post = input('ingrese un mensaje: ')
    s.do({'func':'mensaje', 'data':{'post':post}})
    data = s.receive()

    print(data)

s.close()