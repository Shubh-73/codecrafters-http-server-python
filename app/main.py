# Uncomment this to pass the first stage
import socket

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Create a TCP server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)
    print("Server listening on port 4221...")

    while True:
        # Accept incoming connections
        client_socket, addr = server_socket.accept()
        with client_socket:
            print(f"Connection from {addr}")
            request = client_socket.recv(1024).decode('utf-8')
            print(f"Received request: {request}")

            # Send HTTP 200 OK response
            response = 'HTTP/1.1 200 OK\r\n\r\n'
            client_socket.sendall(response.encode('utf-8'))



if __name__ == "__main__":
    main()
