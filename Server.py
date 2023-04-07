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
        try:
            client = user[1]
            client.sendall(msg.encode())
        except:
            pass

#Handles Peer to Peer Dm
def private_msg(client, msg, userName):
    final_msg = f'[Dm][{userName}]-->{msg}'
    print(final_msg)
    client.sendall(final_msg.encode())


#Listening to messages from client
def listen_message(userName, client, option):

    while True:
        message = client.recv(50000).decode('utf-8')
        final_msg = f'[{userName}]-->{message}'
        if option == -1:
            send_message_to_all(final_msg)
        else:
            private_msg(CLIENT_LIST[option-1][1], message, userName)

#Repeadedly Sends Choice
def option_handler(client):
    while True:
        option = int(client.recv(50000).decode('utf-8'))
        if option==0:
            send_choice(client)
        else:
            return option
    
#Sending the Clients connected
def send_choice(client):
    data = ""
    for user in CLIENT_LIST:
        data += f"{user[0]}+"
    client.sendall(data.encode())

#To get username
def client_handler(client):

    while True:
        userName = client.recv(50000).decode('utf-8')
        if userName != '':
            print("Username Done!")
            CLIENT_LIST.append((userName, client))
            break
    send_choice(client)
    option = option_handler(client)
    threading.Thread(target=listen_message, args=(userName, client, option)).start()
    

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