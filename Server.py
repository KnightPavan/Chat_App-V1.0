import socket
import threading

IP = "192.168.1.10" #Change it to your ip address
PORT = 1234 #Change if not available
LIST_LIMIT = 5
CLIENT_LIST = []

#Send the message received from client to all other users
def send_message_to_all(msg):
    print(msg)
    for user in CLIENT_LIST:
        client = user[1]
        client.sendall(msg.encode())

#Listening to messages from client
def listen_message(userName, client):

    while True:
        message = client.recv(10000).decode('utf-8')
        final_msg = f'{userName}-->{message}'
        send_message_to_all(final_msg)

#To get username
def client_handler(client):

    while True:
        userName = client.recv(10000).decode('utf-8')
        if userName != '':
            print("Username Done!")
            CLIENT_LIST.append((userName, client))
            break

    threading.Thread(target=listen_message, args=(userName, client)).start()

def main():
    #Creating socket object with IPV4 and TCP protocol
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((IP,PORT)) 
        print("Bind Successful")
        server.listen(LIST_LIMIT)
        #To Handle multiple clients
        while True:
            client, address = server.accept()  
            print(f'Successfully connected to {address[0]} : {address[1]}')
            threading.Thread(target=client_handler, args=(client, )).start()

    except:
        print("Bind Unsuccessful!")

    

if __name__ == "__main__":
    main()