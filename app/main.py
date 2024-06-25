# Uncomment this to pass the first stage
import socket
import traceback

def start_server(host = '0.0.0.0', port = 4221):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(5)
        print(f'Server is listening on {port}... ')


        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f'Connected by: {addr}')
                    req = conn.recv(1024).decode('utf-8')
                    print(f'Request: {req}')
                    res = "HTTP/1.1 200 OK\r\n\r\n"
                    conn.sendall(res.encode('utf-8'))
            except Exception as e:
                print(f'Error: {e}')
                traceback.print_exc()
                conn.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.accept()



if __name__ == "__main__":
    start_server()
