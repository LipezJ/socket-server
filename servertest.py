import socket

# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asociar el socket a una dirección IP y puerto
server_socket.bind(('0.0.0.0', 1234))

# Escuchar conexiones entrantes
server_socket.listen()

# Crear una lista para almacenar los sockets de los clientes conectados
client_sockets = []

while True:
    # Aceptar una conexión
    client_socket, client_address = server_socket.accept()
    print('Conexión desde: ', client_address)
    client_sockets.append(client_socket)
    print(client_sockets)

    # Recibir datos del cliente
    data = client_socket.recv(1024)
    print('Recibido: ', data.decode())

    # Enviar datos al cliente
    client_socket.send(data)