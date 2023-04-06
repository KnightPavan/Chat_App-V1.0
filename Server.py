import socket
import threading
IP = "192.168.1.10"
PORT = 1234
LIST_LIMIT = 5
CLIENT_LIST = []

def listen_message(userName, client):

    while True:
        message = client.recv(2048).decode('utf-8')
        final_msg = f'{userName} --> {message}'
        send_message_to_all(final_msg)

def send_message_to_all(msg):

    for user in CLIENT_LIST:
        client = user[1]
        client.sendall(msg.encode())

def client_handler(client):

    while True:
        userName = client.recv(2048).decode('utf-8')
        if userName != '':
            print("Username Done!")
            CLIENT_LIST.append((userName, client))
            break
        else:
            print("Username not found")
    threading.Thread(target=listen_message, args=(userName, client))

def main():

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((IP,PORT))
        print("Bind Successful")
        server.listen(LIST_LIMIT)

        while True:
            client, address = server.accept()
            
            print(f'Successfully connected to {address[0]} : {address[1]}')
            threading.Thread(target=client_handler, args=(client, )).start()

    except:
        print("Bind Unsuccessful!")

    

if __name__ == "__main__":
    main()