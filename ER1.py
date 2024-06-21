from random import randint, choice
import socket
import sqlite3
from signal import signal, SIGINT
import sys

def person():
    return (f'{randint(0,100)}', f'{randint(0,100)}', f'{randint(0,100)}')

def signal_handler(sig, frame):
    sys.exit(0)

def create_database():
    conn = sqlite3.connect("ER1.db")
    cursor = conn.cursor()
    creation_query = '''
    CREATE TABLE IF NOT EXISTS Line (Name, Gender, Room)
    '''
    cursor.execute(creation_query)
    person = ('Dave Johnson', 'Male', 'Xray')
    write_query = '''
    INSERT INTO Line (Name, Gender, Room)
    VALUES (?, ?, ?)
    
    '''
    cursor.execute(write_query, person)
    conn.commit()
    conn.close()

def start_server(host='127.0.0.1', port=1111):
    conn = sqlite3.connect("ER1.db")
    cursor = conn.cursor()
    adding_query = '''
            INSERT INTO Line (Name, Gender, Room)
            VALUES (?, ?, ?)
            '''




    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen()

        signal(SIGINT, signal_handler)


        while True:
            connect, addr = server.accept()
            data = connect.recv(1024).decode()
            if data.split(" ")[0] == 'GET':
                roll = randint(1, 20)
                if roll == 20:
                    cursor.execute(adding_query, person())
                    cursor.execute(adding_query, person())
                if roll > 12:
                    cursor.execute(adding_query, person())
                if roll == 1:
                    cursor.execute("SELECT rowid FROM Line ORDER BY Name LIMIT 2")
                    rows = cursor.fetchall()
                    for row in rows:
                        cursor.execute("DELETE FROM Line WHERE rowid = ?", (row[0],))
                if roll < 8:
                    cursor.execute("SELECT rowid FROM Line ORDER BY Name LIMIT 1")
                    row = cursor.fetchone()
                    cursor.execute("DELETE FROM Line WHERE rowid = ?", (row[0],))
                conn.commit()
                selection_query = '''
                SELECT COUNT(*) FROM Line
                '''
                cursor.execute(selection_query)
                row = cursor.fetchone()
                message = f"{row[0]}"
                connect.sendall(message.encode())
                connect.close()


create_database()
start_server()
