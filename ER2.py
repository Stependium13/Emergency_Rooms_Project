import socket
import sqlite3
from signal import signal, SIGINT
from random import randint
import sys

def signal_handler(sig, frame):
    sys.exit(0)

def start_server(host='127.0.0.1', port=2222):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()

        signal(SIGINT, signal_handler)


        while True:
            conn, addr = server.accept()
            data = conn.recv(1024).decode()
            if data.split(" ")[0] == 'GET':
                message = f"{randint(1, 5)}"
                conn.sendall(message.encode())
                conn.close()



start_server()