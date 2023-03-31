import socket

HOST = "localhost"
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))

    client_id = str(client_socket.getsockname())
    print(f"Welcome to the library, client {client_id}. Type 'exit' to quit.")
    while True:
        request = input("> ")
        client_socket.send(request.encode())

        response = client_socket.recv(1024).decode()
        print(response)

        if request.lower() == "exit":
            break