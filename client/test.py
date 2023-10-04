import socket, time, threading

# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 5500
BUFSIZE = 512 # default maximum size for messages
ADDR = (HOST, PORT)
MESSAGES_TO_SEND = ["Woiro", "Siemanko mordeczki", "{quit}"]

# GLOBAL VARIABLES
MESSAGES_RECEIVED = []

def receive_messages(sock):
    while True:
        try:
            mssg = sock.recv(BUFSIZE).decode('utf8')
            MESSAGES_RECEIVED.append(mssg)
            print(mssg)
            if mssg == '':
                break
        except Exception as e:
            print("[EXCEPTION] ", e)
            break
        
def send_messages(sock):
    for mssg in MESSAGES_TO_SEND:
        time.sleep(1)
        sock.sendall(mssg.encode('utf8'))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(ADDR)
    receiver_thread = threading.Thread(target=receive_messages, args=(s, ))
    sender_thread = threading.Thread(target=send_messages, args=(s, ))

    receiver_thread.start()
    sender_thread.start()

    sender_thread.join()
    receiver_thread.join()