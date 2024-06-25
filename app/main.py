# Uncomment this to pass the first stage
import socket


def handle_request(client_socket):
    client_socket.recv(1024)

    response = "HTTP/1.1 200 OK\r\n\r\n"
    client_socket.send(response.encode())

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()

    try:
        while True:
            print("Waiting for a connection...")
            client_socket, addr = server_socket.accept()
            handle_request(client_socket)
            client_socket.close()

    except KeyboardInterrupt:
        print("^C received, shutting down the web server...")
    finally:
        server_socket.close()
        print("Server closed the server!")






if __name__ == "__main__":
    main()
