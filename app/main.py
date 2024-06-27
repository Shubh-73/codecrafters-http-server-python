import socket
from threading import Thread
import os
import sys

def reply(req, code, body="", headers={}):
    b_reply = b""
    match code:
        case 200:
            b_reply += b"HTTP/1.1 200 OK\r\n"
        case 404:
            b_reply += b"HTTP/1.1 404 Not Found\r\n"
        case 500:
            b_reply += b"HTTP/1.1 500 Internal Server Error\r\n"

    if "Content-Type" not in headers:
        headers["Content-Type"] = "text/plain"
    if body != "":
        headers["Content-Length"] = str(len(body))

    for key, value in headers.items():
        b_reply += bytes(f"{key}: {value}\r\n", "utf-8")
    b_reply += b"\r\n" + bytes(body, "utf-8")
    return b_reply

def parse_request(bytes_data):
    """Parse the HTTP request and extract the method, path, and headers."""
    output = {"method": "", "path": "", "headers": {}, "body": ""}
    lines = bytes_data.decode("utf-8").split("\r\n")

    if len(lines) < 3:
        return None
    reqLine = lines[0].split(" ")
    if not reqLine[0] or reqLine[0] not in ["GET", "POST", "PUT", "DELETE"]:
        return None
    if not reqLine[1] or reqLine[1][0] != "/":
        return None
    output["method"] = reqLine[0]
    output["path"] = reqLine[1]

    lines = lines[1:]
    c = 0
    for line in lines:
        if line == "":
            break
        headline = line.split(":")
        output["headers"][headline[0]] = headline[1].lstrip()
        c += 1
    if len(lines) > c + 1:
        output["body"] = lines[c + 1]
    return output

def handle_request(conn, req, directory_path):
    """Generate an appropriate HTTP response based on the request path."""
    if req["path"] == "/":
        return reply(req, 200)
    if req["path"].startswith("/echo"):
        return reply(req, 200, req["path"][6:])
    if req["path"] == "/user-agent":
        ua = req["headers"]["User-Agent"]
        return reply(req, 200, ua)
    if req["path"].startswith("/files"):
        filename = req["path"][7:]
        file_path = os.path.join(directory_path, filename)

        try:
            with open(file_path, "r") as f:
                body = f.read()
            headers = {
                "Content-Type": "application/octet-stream",
                "Content-Length": str(len(body))
            }
            return reply(req, 200, body, headers)
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return reply(req, 404)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return reply(req, 500)
    return reply(req, 404)

def handle_client(conn, directory_path):
    try:
        byte_data = conn.recv(1024)
        if byte_data:
            parsed_req = parse_request(byte_data)
            if parsed_req is None:
                conn.sendall(reply(None, 500))
            else:
                conn.sendall(handle_request(conn, parsed_req, directory_path))
    except Exception as e:
        print(f"Connection closed unexpectedly: {e}")
    finally:
        conn.close()

def main():
    # Parse the --directory flag
    if len(sys.argv) != 3 or sys.argv[1] != "--directory":
        print("Usage: ./your_server.sh --directory <directory_path>")
        sys.exit(1)

    directory_path = sys.argv[2]

    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        sys.exit(1)

    print(f"Serving files from directory: {directory_path}")

    # Create a TCP server socket
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    threads = []

    while True:
        conn, addr = server_socket.accept()
        t = Thread(target=handle_client, args=(conn, directory_path))
        threads.append(t)
        t.start()

if __name__ == "__main__":
    main()
