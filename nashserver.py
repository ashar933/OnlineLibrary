import socket
import datetime
import threading

books = {
    "Harry Potter": "",
    "Percy Jackson": "",
    "Famous Five": "",
    "Secret Seven": "",
    "Narnian Chronicles": "",
}

def calculate_due_date():
    return datetime.date.today() + datetime.timedelta(days=14)

def handle_request(connection, address):
    client_id = str(address)
    while True:
        data = connection.recv(1024).decode()

        if not data or data.lower() == "exit":
            break

        if data.startswith("borrow "):
            book = data.split(" ")[1]+" "+data.split(" ")[2]
            if book in books and not books[book]:
                due_date = str(calculate_due_date())
                books[book] = (client_id, due_date)
                connection.send(f"{book} borrowed. Due date: {due_date}".encode())
            else:
                connection.send(f"{book} is not available".encode())
        elif data.startswith("return "):
            book = data.split(" ")[1]+" "+data.split(" ")[2]
            if book in books and books[book][0] == client_id:
                books[book] = ""
                connection.send(f"{book} returned".encode())
            else:
                connection.send(f"{book} cannot be returned".encode())
        elif data == "list":
            book_list = "\n".join([f"{book}: {due_date[1]}" for book, due_date in books.items() if due_date])
            connection.send(book_list.encode())
        else:
            connection.send("Invalid request".encode())

    connection.close()

HOST = ""
PORT = 8000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Server listening on port {PORT}")

    while True:
        connection, address = server_socket.accept()
        print(f"Connected by {address}")

        client_thread = threading.Thread(target=handle_request, args=(connection, address))
        client_thread.start()