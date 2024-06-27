import socket
import threading
import sys
import os

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

def parse_request(request: str):
    """Parse the HTTP request and extract the method, path, and headers."""
    header_dict = {"headers": {}}
    headers = request.split("\r\n")
    request_line = headers[0].split()

    header_dict["method"] = request_line[0]
    header_dict["path"] = request_line[1]
    header_dict["protocol"] = request_line[2]

    for header in headers[1:]:
        if header == "":
            break
        else:
            key, value = header.split(":", 1)
            header_dict["headers"][key.strip()] = value.strip()
    header_dict["data"] = headers[-1].strip()
    return header_dict

def handle_client(client):
    try:
        request = client.recv(1024).decode("utf-8")
        parsed_request = parse_request(request)

        if len(sys.argv) > 1 and sys.argv[1] == "--directory":
            directory = sys.argv[2]

        modified_path = parsed_request["path"].split("/", 2)

        if modified_path[1] == "echo":
            client.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(modified_path[2])}\r\n\r\n{modified_path[2]}".encode("utf-8")
            )
        elif modified_path[1] == "files":
            filename = modified_path[2]
            filepath = os.path.join(directory, filename)

            if parsed_request["method"] == "GET":
                if os.path.exists(filepath):
                    with open(filepath, "r") as f:
                        content = f.read()
                    client.sendall(
                        f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode("utf-8")
                    )
                else:
                    client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
            elif parsed_request["method"] == "POST":
                with open(filepath, "w") as f:
                    f.write(parsed_request["data"])
                client.sendall(b"HTTP/1.1 201 Created\r\n\r\n")
        elif parsed_request["path"] == "/":
            client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        elif parsed_request["path"] == "/user-agent":
            user_agent = parsed_request["headers"].get("User-Agent", "").strip()
            client.sendall(
                f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode("utf-8")
            )
        else:
            client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")
    except Exception as e:
        print(f"Exception handling request: {e}")
    finally:
        client.close()

def main():
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    while True:
        client, address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()
