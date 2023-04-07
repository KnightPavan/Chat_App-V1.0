import socket
import threading

IP = "192.168.1.10" #Change ip and port number to that of the server
PORT = 1234

#To listen to the messages from other users
def msg_listner(client, myUserName):
    while True:
        msg = client.recv(50000).decode('utf-8')
        userName = msg.split("-->")[0]
        content = msg.split("-->")[1]
        Name = myUserName
        if userName[:4]!= "[Dm]":
            Name = f"[{myUserName}]"

        if (userName != Name):
            print(f"{userName} {content}")

#To send the username to the server
def initial_msg(client):
    userName = input("Enter UserName : ")
    if userName != '':
        client.sendall(userName.encode())
    else:
        print("UserName Invalid. Please enter the correct UserName")
    return userName

#To send the messages to the server
def msg_send(client):
    while True:
        msg = input(">>> ")
        client.sendall(msg.encode())

#Handles Options
def msg_routing(client, userName):
    
    while True:
        data = client.recv(50000).decode('utf-8')
        list = data.split("+")
        print(" 0. Reload Clients")
        print("-1. Broadcast To All")
        for i in range(1, len(list)):
            print(f" {i}. {list[i-1]}")
        
        option = str(input("Enter your choice : "))
        client.sendall(option.encode())
        if int(option) != 0:
            break
    

def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # try:
    client.connect((IP, PORT))
    print("Connection established successfully")
    userName = initial_msg(client)
    
    msg_routing(client, userName)
    threading.Thread(target=msg_listner, args=(client, userName)).start()
    threading.Thread(target=msg_send, args=(client, )).start()
    # except :
    #     print("Unsuccessfull")
    

if __name__ == "__main__":
    main()