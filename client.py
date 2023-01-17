import socket
import pickle
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("localhost", 12345))

for i in range(10):
    s.send(pickle.dumps({'func':'sumar', 'data':{'num1': 1, 'num2': i}}))

    data = pickle.loads(s.recv(1024))
    print("Received data:", data)

    time.sleep(1)

s.close()