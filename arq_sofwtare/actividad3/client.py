import socket

# Configuración del cliente
host = '127.0.0.1'  # Dirección IP del servidor
port = 12345        # Puerto del servidor

#Crear un socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectarse al servidor
client_socket.connect((host, port))

print("Conectado al servidor. Escribe 'exit' para cerrar la conexión.")

# Enviar y recibir mensajes.
while True:
    # Pedir al usuario que ingrese un mensaje
    message = input("Ingrese mensaje para el servidor: ")
    
    # Si el mensaje es 'exit', cerrar la conexión
    if message.lower() == 'exit':
        print("Cerrando conexión...")
        break
    
    # Enviar el mensaje al servidor
    client_socket.send(message.encode())

    # Recibir la respuesta del servidor
    data = client_socket.recv(1024).decode()
    print(f"Respuesta del servidor: {data}")

# Cerrar la conexión
client_socket.close()
