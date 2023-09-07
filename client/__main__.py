from .client import Client
import sys


LOCAL_IP = '127.0.0.1'
LOCAL_PORT = 55555


if __name__ == "__main__":
    client = Client(LOCAL_IP, LOCAL_PORT)
    client.start()

