import socket
import pickle
import time
import threading
import select

sockets = []

def sumar(data): 
    return data['num1'] + data['num2']
def mensaje(data):
    print(data['post'])
    return 'post sucess'
    
funcs = {'sumar':sumar, 'mensaje':mensaje}

def handleClient():
    while True:
        for socket in sockets:
            handleSocket(socket)
            handleDisconnect(socket)

def handleDisconnect(client):
    readable, _, exceptional = select.select([client], [], [client], 0)
    for s in exceptional:
        clients.remove(s)
        s.close()
        print(s, 'desconectado')

def handleSocket(client):
    client.settimeout(0.1)
    try:
        data = client.recv(1024)
        if not data:
            return 0
        data = pickle.loads(data)
        if data['func'] in funcs:
            result = funcs[data['func']](data['data'])
            client.send(pickle.dumps({'result':result}))
    except (ConnectionResetError, KeyboardInterrupt):
        print(client, 'desconectado')
        sockets.remove(client)
        return 0
    except socket.timeout:
        return 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", 12345))

s.listen()

t = threading.Thread(target=handleClient)
t.start()

while True:
    client, address = s.accept()
    print(client, address, client not in sockets)
    if client not in sockets:
        sockets.append(client)