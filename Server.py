import socket

def start_client():

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            host = '127.0.0.1'
            id = input("Which ER you want to check: ")
            message = f"GET Total FROM {id}"
            port = int(id) * 1111
            client.connect((host, port))
            client.sendall(message.encode())
            data = client.recv(1024)
            if data:
                print(f"ER{id} now has total of {data.decode()} customers in line.\n")
            client.close()


start_client()


