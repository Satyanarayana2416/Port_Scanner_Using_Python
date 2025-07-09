import socket
import threading

clients = []

def handle_client(conn):
    while True:
        try:
            msg = conn.recv(4096)
            for client in clients:
                if client != conn:
                    client.send(msg)
        except:
            clients.remove(conn)
            break

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9999))
server.listen()

print("Server started...")

while True:
    conn, addr = server.accept()
    clients.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()
