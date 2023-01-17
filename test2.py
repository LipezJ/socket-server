import socket
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
s.connect(("localhost", 12345))

t = True
post = ' '

while len(post) > 0 or t:
    t = False

    post = input('ingrese un mensaje: ')

    s.send(pickle.dumps({'func':'mensaje', 'data':{'post':post}}))
    data = pickle.loads(s.recv(1024))
    print(data)

s.close()