import socket

import threading

import sys

# def parse_request(request_data):

#     lines = request_data.split('\r\n')

#     start_line = lines[0]

#     method, path, version = start_line.split(' ')

#     return method, path, version

# def get_response(path):

#     responses = {

#     "/" : "HTTP/1.1 200 OK\r\n\r\n",

#     }

#     default_response = "HTTP/1.1 404 Not Found\r\n\r\n"

#     return responses.get(path, default_response)

def read_file(directory, filename):

    with open(f"/{directory}/{filename}", "r") as f:

        data = f.read()

    return data

def handle_request(conn, addr):

    data = conn.recv(1024).decode()

    request_data = data.split("\r\n")

    path = request_data[0].split(" ")[1]

    if path == "/":

        response = b"HTTP/1.1 200 OK\r\n\r\n"

    elif path.startswith("/echo"):

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(path[6:])}\r\n\r\n{path[6:]}".encode()

    elif path == "/user-agent":

        user_content = request_data[2].split(" ")[1]

        response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_content)}\r\n\r\n{user_content}".encode()

    elif path.startswith("/files"):

        directory = sys.argv[2]

        file_name = path[7:]

        try:

            data = read_file(directory, file_name)

            response = f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(data)}\r\n\r\n{data}".encode()

        except Exception as e:

            response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    else:

        response = b"HTTP/1.1 404 Not Found\r\n\r\n"

    conn.sendall(response)

    conn.close()

def main():

    # You can use print statements as follows for debugging, they'll be visible when running tests.

    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage

    server_socket = socket.create_server(("localhost", 4221))

    while True:

        conn, addr = server_socket.accept()  # wait for client

        thread = threading.Thread(target=lambda: handle_request(conn, addr))

        thread.start()

if __name__ == "__main__":

    main()