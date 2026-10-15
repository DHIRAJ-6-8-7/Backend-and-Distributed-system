from urllib.parse import urlsplit, parse_qs
import socket
import json

HOST = "127.0.0.1"
PORT = 8000


def handle_request(request):
    request_line = request.splitlines()[0]
    method, target, version = request_line.split()

    parsed_url = urlsplit(target)
    path = parsed_url.path
    query = parse_qs(parsed_url.query)

    print(f"Method: {method}")
    print(f"Path: {path}")
    print(f"HTTP version: {version}")

    headers_extra = ""

    if path != "/tasks":
        status = "404 Not Found"
        data = {"error": "Resource not found"}

    elif method not in ("GET", "HEAD"):
        status = "405 Method Not Allowed"
        data = {"error": "Method not allowed"}
        headers_extra = "Allow: GET, HEAD\r\n"

    else:
        raw_limit = query.get("limit", ["2"])[0]

        try:
            limit = int(raw_limit)

            if limit < 1 or limit > 100:
                raise ValueError

        except ValueError:
            status = "400 Bad Request"
            data = {"error": "limit must be an integer between 1 and 100"}

        else:
            status = "200 OK"
            data = {
                "tasks": [
                    {"id": 1, "title": "Learn HTTP"},
                    {"id": 2, "title": "Build TaskFlow"},
                ][:limit]
            }

    body = json.dumps(data).encode("utf-8")

    headers = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        f"{headers_extra}"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")

    if method == "HEAD":
        return headers

    return headers + body

    request_line = request.splitlines()[0]
    method, target, version = request_line.split()

    parsed_url = urlsplit(target)
    path = parsed_url.path
    query = parse_qs(parsed_url.query)

    print(f"Method: {method}")
    print(f"Path: {path}")
    print(f"HTTP version: {version}")

    headers_extra = ""

    if path == "/tasks":
        data = {
            "tasks": [
                {"id": 1, "title": "Learn HTTP"},
                {"id": 2, "title": "Build TaskFlow"},
            ]
        }
        raw_limit = query.get("limit", ["2"])[0]

        try:
            limit = int(raw_limit)

            if limit < 1 or limit > 100:
                raise ValueError
        except ValueError:
            status = "400 Bad Request"
            data = {"error": "Invalid limit value"}
        else:
            data["tasks"] = data["tasks"][:limit]
        if method in ("GET", "HEAD"):
            status = "200 OK"
        else:
            status = "405 Method Not Allowed"
            data = {"error": "Method not allowed"}
            headers_extra = "Allow: GET, HEAD\r\n"
    else:
        status = "404 Not Found"
        data = {"error": "Resource not found"}

    body = json.dumps(data).encode("utf-8")

    headers = (
        f"HTTP/1.1 {status}\r\n"
        "Content-Type: application/json\r\n"
        f"Content-Length: {len(body)}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).encode("utf-8")

    if method == "HEAD":
        return headers

    return headers + body


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()

        print(f"Server listening at http://{HOST}:{PORT}")

        while True:
            client, address = server.accept()

            with client:
                print(f"\nConnection from: {address}")

                request = client.recv(4096).decode("utf-8")
                print("Received HTTP request:")
                print(request)

                response = handle_request(request)
                client.sendall(response)


if __name__ == "__main__":
    main()
