import threading
from .manager import Manager
from .client import Client
from typing import List
import json

class Handler:
    
    def __init__(self, clientDict):
        # Initialize the Handler with a dictionary to manage connected clients.
        self.database = Manager("sqlite:///database.db")
        # Create ten lobbies when initializing the Handler.
        for index in range(10):
            self.database.create_lobby(f'lobby{index}')
        self.clientDict = clientDict
    
    def handle_clients(self, server, closing):
        try:
            # Accept a new client connection.
            client, address = server.accept()
            print(f'Connected with {str(address)}')
            # If the server is not closing, start a new thread to handle the client.
            if not closing:
                thread = threading.Thread(target=self.handle_client, args=(client, address))
                thread.start()
            
        except OSError as e:
            if not closing:
                print(f"Error accepting client: {e}")

    def handle_client(self, client, address):
        # Create a Client instance to handle the communication with the connected client.
        client = Client(client, address, self.clientDict, self.database)
        # Call the handler method of the Client instance to manage client interactions.
        client.handler()
