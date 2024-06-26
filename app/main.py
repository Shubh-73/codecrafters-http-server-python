# Uncomment this to pass the first stage
import socket
import re

def parse_request(request):
    """Parse the HTTP request and extract the method and path."""
    lines = request.split('\r\n')
    request_line = lines[0]
    method, path, _ = request_line.split()
    return method, path

def handle_request(method, path):
    """Generate an appropriate HTTP response based on the request path."""
    if method == 'GET':
        if path == '/':
            return 'HTTP/1.1 200 OK\r\n\r\n'
        elif path.startswith('/echo/'):
            # Extract the string parameter from the path
            match = re.match(r'/echo/(.+)', path)
            if match:
                echoed_string = match.group(1)
                content_length = len(echoed_string)
                headers = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n'
                return headers + echoed_string
            else:
                return 'HTTP/1.1 404 Not Found\r\n\r\n'
        elif path == '/user-agent':
            user_agent = headers.get('User-Agent', '')
            content_length = len(user_agent)
            response_headers = f'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {content_length}\r\n\r\n'
            return response_headers + user_agent
        else:
            return 'HTTP/1.1 404 Not Found\r\n\r\n'
    else:
        return 'HTTP/1.1 405 Method Not Allowed\r\n\r\n'


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

            method, path = parse_request(request)
            response = handle_request(method, path)
            client_socket.sendall(response.encode('utf-8'))



if __name__ == "__main__":
    main()
