from socket import socket
from socket import AF_INET, SOCK_STREAM
import time

from person import Person

from threading import Thread

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
BUFSIZE = 512 # default maximum size for messages
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10

# GLOBAL VARIABLES
persons = []
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) # set up server

def broadcast(msg, name=None):
    for person in persons:
        client = person.client
        if name is None:
            client.send(bytes(msg, encoding="utf8"))
        else:
            client.send(bytes(name + ': ' + msg, encoding="utf8"))

def client_communication(person):
    client = person.client
    addr = person.addr

    # Get persons name
    name = client.recv(BUFSIZE).decode("utf8")
    msg = f"{name} has joined the chat!"
    broadcast(msg)

    while True:
        try:
            msg = client.recv(BUFSIZE)
            print(f"{name}: ", msg.decode("utf8"))

            if msg == bytes('{quit}', 'utf8'): # equals to '{quit}'.encode("utf8")
                broadcast(f"{name} has left the chat ...")
                client.send(bytes("{quit}", "utf8"))
                
                client.close()
                print(f"[CONNCETION CLOSED] {addr} closed connection to server at {time.time()}")

                persons.remove(person)
                break
            else:
                broadcast(msg.decode('utf8'), name)
        except Exception as e:
            print("[EXCEPTION]", e)
            break

def wait_for_connection(SERVER):
    run = True
    while run:
        try:
            client, address = SERVER.accept()
            person = Person(address, client)
            persons.append(person)
            print(f"[CONNECTION] {address} connected to server at {time.time()}")
            Thread(target=client_communication, args=(person, )).start()
        except Exception as e:
            print('[EXCEPTION]', e)
            run = False

if __name__ == '__main__':
    SERVER.listen(MAX_CONNECTIONS) # listen for connections
    print('[STARTED] Waiting for connection ...')
    ACCEPT_THREAD = Thread(target=wait_for_connection, args=(SERVER, ))
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()