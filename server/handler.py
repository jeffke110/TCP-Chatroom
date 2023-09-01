import threading
from .manager import Manager
from .client import Client
from typing import List
import json

class Handler:
    
    def __init__(self, clientDict):
        self.database = Manager("sqlite:///database.db")
        for index in range(10):
            self.database.create_lobby(f'lobby{index}')
        self.clientDict = clientDict
    
    
    def handle_clients(self, server, closing):
        try:
            client, address = server.accept()
            print(f'Connected with {str(address)}')
            if not closing:
                thread = threading.Thread(target=self.handle_client, args=(client, address))
                thread.start()
            
        except OSError as e:
            if not closing:
                print(f"Error accepting client: {e}")
    

    def handle_client(self, client, address):
        client = Client(client, address, self.clientDict, self.database)
        client.handler()
