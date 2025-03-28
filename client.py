import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))   

name = input("Enter your name: ")

def receive():
    while True:
        try:
            message, addr = client.recvfrom(1024)
            print(message.decode())
        except Exception as e:
            print(f"Receive error: {e}")
            break  # Exit thread if an error occurs

# Start receiving thread
t = threading.Thread(target=receive, daemon=True)  
t.start()

# Notify server about signup
client.sendto(f"SIGNUP_TAG:{name}".encode(), ('localhost', 9999))

# Main loop for sending messages
try:
    while True:
        message = input("> ")  # Prompt for clarity
        if message.strip() == "!q":
            print("Exiting chat...")
            break
        client.sendto(f"{name}: {message}".encode(), ('localhost', 9999))
except KeyboardInterrupt:
    print("\nInterrupted! Exiting chat...")

# Cleanup
client.close()
