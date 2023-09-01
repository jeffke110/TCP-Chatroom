from .handler import Handler
import threading
import socket
from typing import List
import logging

logger = logging.getLogger(__name__)


class Server:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clientDict : dict[str, List]  = { 
                "lobby0" : [], "lobby1" : [],
                "lobby2" : [], "lobby3" : [],
                "lobby4" : [], "lobby5" : [],
                "lobby6" : [], "lobby7" : [],
                "lobby8" : [], "lobby9" : []}
        self.server = None
        self.manager = Handler(self.clientDict)

    def setup_server(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f'Server listening on port {self.host}:{self.port}')

    def debug_input(self):
        while True:
            message = input()
            if message.lower() == "quit":
                for lobby_name in self.clientDict:
                    for client in self.clientDict[lobby_name]:
                        client.close()
                self.server.close()
                       
    def accept_clients(self):
        self.setup_server()
        debug_input_thread = threading.Thread(target=self.debug_input)
        debug_input_thread.start()
        while True:
            self.manager.handle_clients(self.server)
            
    def shutdown(self):
        print("\n Shutting down server..")
        for lobby_name in self.clientDict:
            for client in self.clientDict[lobby_name]:
                    client.close()
        self.server.close()