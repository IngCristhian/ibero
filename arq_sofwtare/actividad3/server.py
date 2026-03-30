import socket

# Configuración del servidor
host = '127.0.0.1'  # Dirección IP del servidor (localhost)
port = 12345        # Puerto del servidor

# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket al host y al puerto
server_socket.bind((host, port))

# Poner el servidor en modo de escucha
server_socket.listen(1)
print(f"Servidor escuchando en {host}:{port}...")

# Aceptar conexión del cliente
client_socket, client_address = server_socket.accept()
print(f"Conexión establecida con {client_address}")

# Ciclo para recibir mensajes del cliente
while True:
    # Recibir mensaje del cliente
    data = client_socket.recv(1024).decode()
    if not data:
        break
    print(f"Mensaje recibido del cliente: {data}")

    # Responder al cliente
    response = f"Mensaje recibido correctamente: {data}"
    client_socket.send(response.encode())

# Cerrar la conexión
client_socket.close()
server_socket.close()