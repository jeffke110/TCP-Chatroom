import socket
import threading
from typing import List, Dict
from .handler import Handler

class Server:

    def __init__(self, host, port):
        # Initialize the Server instance with the host and port.
        self.host = host
        self.port = port
        # Dictionary to store connected clients in different lobbies.
        self.clientDict: Dict[str, List] = {
            "lobby0": [], "lobby1": [],
            "lobby2": [], "lobby3": [],
            "lobby4": [], "lobby5": [],
            "lobby6": [], "lobby7": [],
            "lobby8": [], "lobby9": []
        }
        self.server = None
        self.manager = Handler(self.clientDict)
        self.closing = False  # Flag to indicate server shutdown

    def setup_server(self):
        # Create and configure the server socket.
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen()
        print(f'Server listening on port {self.host}:{self.port}')

    def debug_input(self):
        # Debug input thread for server shutdown.
        while not self.closing:
            message = input()
            if message.lower() == "quit":
                self.shutdown()

    def accept_clients(self):
        # Start accepting client connections and handle them.
        self.setup_server()
        debug_input_thread = threading.Thread(target=self.debug_input)
        debug_input_thread.start()
        while not self.closing:
            self.manager.handle_clients(self.server, self.closing)

    def shutdown(self):
        # Shutdown the server gracefully.
        print("\nShutting down server...")
        self.closing = True  # Set the closing flag
        # Close all client connections.
        for lobby_name in self.clientDict:
            for client in self.clientDict[lobby_name]:
                client.close()
        self.server.close()

if __name__ == "__main__":
    # Create and start the server.
    server = Server("127.0.0.1", 55555)
    server.accept_clients()
