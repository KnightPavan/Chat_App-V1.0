import socket

IP = "192.168.1.10"
PORT = 1234

def main():
    
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))
        print("Connection established successfully")
    except:
        print("Error")

if __name__ == "__main__":
    main()