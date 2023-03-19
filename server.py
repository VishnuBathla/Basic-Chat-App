import socket
import threading
host="127.0.0.1"
port=9090 #udp
server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
client={}
def broadcast(message):
    for i in client:
        i.send(message)
def handle(cl):
    while True:
        try:
            message=cl.recv(1024)
            print(f'{client[cl]} says {message}')
            broadcast(message)
        except:
            cl.close()
            if(cl in client):
                del client[cl]
            break
def receive():
    while True:
        cl,address=server.accept()
        print(f"Connected with {address}")
        cl.send("Name".encode('utf-8'))
        nm=cl.recv(1024)
        client[cl]=nm
        print(f"Name of the client is {nm}")
        broadcast(f'{nm} connected to the server!\n'.encode('utf-8'))
        cl.send("Connected to the server\n".encode('utf-8'))
        thread=threading.Thread(target=handle,args=(cl,))
        thread.start()
print("Welcome to the final show, hope you're wearing your best clothes")
receive()
