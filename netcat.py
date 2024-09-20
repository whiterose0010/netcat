import socket
import threading

def handle_client(client_socket):
    with client_socket:
        while True:
            try :
                request = client_socket.recv(4096)
                if not request:
                    print("connection closed by client.")
                    break

                print(f"Received : {request.decode()}")
                response = "Echo : " + request.decode()
                client_socket.send(response.encode())
            except Exception as e:
                print(f"Error : {e}")
                break

def server(host, port):
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Listening on {host}:{port}")

    while True:
        try:
            client_socket, addr = server_socket.accept()
            print(f"Accepted connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
        except Exception as e:
            print(f"Error accepting connection : {e}")

def client(target_host, target_port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((target_host,target_port))
    except Exception as e:
        print(f"Error connecting to server : {e}")
        return

    try:
        while True:
            message = input("Send (type 'exit' to quit) : ")
            if message.lower() == 'exit':
                print("Closing connection.")
                break
            client_socket.send(message.encode())
            response = client_socket.recv(4096)
            print(f"Received: {response.decode()}")
    except KeyboardInterrupt:
        print("\nConnection closed by user")
    except Exception as e:
        print(f"Error : {e}")
    finally:
        client_socket.close()
        print("Client socket closed.")

if __name__ == "__main__":
    mode = input("Run as server (s) or client (c)?")

    if mode.lower() == 's':
        host = input("Enter host to listen on : ")
        port = int(input("Enter port to listen on : "))
        server(host,port)
    elif mode.lower() == 'c':
        target_host = input("Enter target host : ")
        target_port = int(input("Enter target port : "))
        client(target_host,target_port)
    else:
        print("Invalid option. Please choose 's' or 'c'.")