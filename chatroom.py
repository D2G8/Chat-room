import socket
import threading
import queue

message = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('localhost', 9999))

def receive():
    while True:
        try:
            msg, addr = server.recvfrom(1024)
            message.put((msg, addr))
        except Exception as e:
            print(f"Receive error: {e}")

def broadcast():
    while True:
        while not message.empty():
            msg, addr = message.get()
            print(msg.decode())

            if addr not in clients:
                clients.append(addr)

            for client in clients:
                try:
                    if msg.decode().startswith("SIGNUP_TAG:"):
                        name = msg.decode().split(":", 1)[1]  # Extract name
                        server.sendto(f"{name} joined!".encode(), client)
                    else:
                        server.sendto(msg, client)
                except Exception as e:
                    print(f"Error sending to {client}: {e}")
                    clients.remove(client)

# Start threads
t1 = threading.Thread(target=receive, daemon=True)
t2 = threading.Thread(target=broadcast, daemon=True)

t1.start()
t2.start()

# Keep the main thread alive
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Server shutting down.")
