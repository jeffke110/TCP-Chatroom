from .server import Server
import sys

LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 55555


if __name__ == "__main__":
    server = Server(LOCAL_IP, LOCAL_PORT)
    server.accept_clients()