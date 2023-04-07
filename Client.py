import socket
import threading

IP = "192.168.1.10"
PORT = 1234

#To listen to the messages from other users
def msg_listner(client, myUserName):
    while True:
        msg = client.recv(10000).decode('utf-8')
        userName = msg.split("-->")[0]
        content = msg.split("-->")[1]
        if (userName != myUserName):
            print(f"[{userName}] {content}")

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

def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))
        print("Connection established successfully")
        userName = initial_msg(client)
        
        threading.Thread(target=msg_listner, args=(client, userName)).start()
        threading.Thread(target=msg_send, args=(client, )).start()
    except:
        print("Error")
    

if __name__ == "__main__":
    main()