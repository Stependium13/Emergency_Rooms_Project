import socket
import sqlite3

def create_database(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    creation_query = '''
    CREATE TABLE IF NOT EXISTS clinics (name, Address, PostalCode)
    '''
    cursor.execute(creation_query)
    creation_query = '''
    CREATE TABLE IF NOT EXISTS routes (name, Route)
    '''
    cursor.execute(creation_query)
    adding_query = '''
    INSERT INTO clinics (Name, Address, PostalCode)
    VALUES (?, ?, ?)
    '''

    cursor.execute(adding_query, ('ER1', '123 Main Str', '95610'))
    cursor.execute(adding_query, ('ER2', '823 High Blvd', '73459'))
    cursor.execute(adding_query, ('ER3', '992 Sun Ave', '68512'))
    adding_query = '''
    INSERT INTO routes (Name, Route)
    VALUES (?, ?)
    '''

    cursor.execute(adding_query, ('ER1', '127.0.0.1:1111'))
    cursor.execute(adding_query, ('ER2', '127.0.0.1:2222'))
    cursor.execute(adding_query, ('ER3', '127.0.0.1:3333'))

    conn.commit()

def start_client():

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            conn = sqlite3.connect('Emergency_Rooms.db')
            cursor = conn.cursor()
            id = input("Which ER you want to check: ")
            selection_query = f'''
            SELECT route FROM routes WHERE name = "ER{id}"
            '''
            cursor.execute(selection_query)
            row = cursor.fetchone()
            print(row)
            host, port = row[0].split(':')
            message = f"GET Total FROM {id}"

            client.connect((host, int(port)))
            client.sendall(message.encode())
            data = client.recv(1024)
            if data:
                print(f"ER{id} now has total of {data.decode()} customers in line.\n")
            client.close()

create_database('Emergency_Rooms.db')
start_client()


