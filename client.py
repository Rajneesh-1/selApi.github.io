import socket
from threading import Thread

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = socket.gethostname()
port = 1255
client.connect((host, port))
name = input("Enter Your Name:")
client.send(name.encode())
con = True
def send(client):
    while con:
        data = f'{name}:{input("")}'
        client.send(data.encode())

def receive(client):
    while con:
        try:
            data = client.recv(1024).decode()
            print(data)
        except:
            print("Exception")
            client.close()
            break

thread1 = Thread(target=send, args=(client,))
thread1.start()

thread2 = Thread(target=receive, args=(client,))
thread2.start()
