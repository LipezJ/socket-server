import socket
import pickle
import time

from client import socketClient

s = socketClient('localhost', 8080)
s.connect()

t = True
post = ' '

while True:
    post = input('ingrese un mensaje: ')
    s.do({'func':'mensaje', 'data':{'post':post}})
    data = s.receive()
    if not data:
        continue
    print(data)

s.close()