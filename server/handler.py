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
    
    
    def handle_clients(self, server):
        client, address = server.accept()
        print(f'Connected with {str(address)}')
        
        data = {'TYPE' : 'USERNAME'}
        json_data = json.dumps(data).encode('utf-8')
        client.send(json_data)
        
        self.nickname : str = client.recv(1024).decode('ascii')
        
        while self.database.create_user(self.nickname) == False:
            data = {'TYPE': 'INVALID_USERNAME'}
            json_data = json.dumps(data).encode('utf-8')
            client.send(json_data)
            self.nickname = client.recv(1024).decode('ascii')
            
        self.clientDict["lobby0"].append(client)
           
        # add user to general lobby
        self.database.add_user_to_lobby(self.nickname, "lobby0")
        
        data = {'TYPE' : 'VALIDATED'}
        json_data = json.dumps(data).encode('utf-8')
        client.send(json_data)

        thread = threading.Thread(target=self.handle_client, args=(client,))
        thread.start()
    

    def handle_client(self, client):
        client = Client(client, self.nickname, self.clientDict, self.database)
        client.handler()
