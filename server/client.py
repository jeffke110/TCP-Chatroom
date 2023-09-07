import json
from .manager import Manager

class Client:
    
    def __init__(self, client, address, clientDict, database):
        # Initialize the client with its socket, address, client dictionary, and database manager
        self.client = client
        self.nickname = None
        self.address = address
        self.clientDict = clientDict
        self.database: Manager = database
        self.current_lobby = "lobby0"
        
    def handler(self):
        # Handle client connections and messages
        # Send a request for the client to choose a username
        data = {'TYPE' : 'USERNAME'}
        json_data = json.dumps(data).encode('utf-8')
        self.client.send(json_data)
        
        # Receive the chosen username from the client
        received_object = self.client.recv(1024).decode('utf-8')
        username_message = json.loads(received_object)
        
        if username_message['TYPE'] != "QUIT":
            self.nickname: str = username_message["TYPE"]
        
            # Add the client to the lobby and update the database
            self.clientDict["lobby0"].append(self.client)
            if self.database.create_user(self.nickname) == True:
                self.database.add_user_to_lobby(self.nickname, "lobby0")
            
            # Send a validation message to the client
            data = {'TYPE' : 'VALIDATED'}
            json_data = json.dumps(data).encode('utf-8')
            self.client.send(json_data)

            # Send existing messages and users to the client
            current_messages = self.database.get_messages_in_lobby(self.current_lobby)
            for msg in current_messages:
                data = {'TYPE': 'MESSAGE', "ID": msg.id, "CONTENT": str(msg.content), "USER": str(msg.sender_username), "TIME" : str(msg.time)}
                json_data = json.dumps(data).encode('utf-8')
                self.client.send(json_data + b'\n')  
                        
            current_users = self.database.get_users_in_lobby(self.current_lobby)
            for user in current_users:
                data = {'TYPE': 'USER', 'USERNAME':  str(user.username)}
                json_data = json.dumps(data).encode('utf-8')
                self.client.send(json_data + b'\n')  
                
            while True:
                try:
                    received_object = self.client.recv(1024).decode('utf-8')
                    message = json.loads(received_object)
                    if message['TYPE'] == "MESSAGE":
                        # Broadcast the received message to all clients in the lobby
                        self.broadcast(message["CONTENT"], message["TIME"])
                        self.database.create_message(message["CONTENT"], message["LOBBY"], self.nickname, message["TIME"])
                    elif message['TYPE'] == "QUIT":
                        # Handle client disconnection
                        for key in self.clientDict:
                            self.clientDict[key] = [item for item in self.clientDict[key] if item != self.client]
                        self.client.close()
                        break
                    elif message['TYPE'] == "CHANGE_LOBBY":
                        # Handle lobby change request
                        self.clientDict[self.current_lobby].remove(self.client)
                        self.current_lobby = message["LOBBY"]
                        self.clientDict[self.current_lobby].append(self.client)
                        self.database.add_user_to_lobby(self.nickname, self.current_lobby)
                        
                        # Send existing messages and users in the new lobby to the client
                        current_messages = self.database.get_messages_in_lobby(self.current_lobby)
                        for msg in current_messages:
                            data = {'TYPE': 'MESSAGE', "ID": msg.id, "CONTENT": str(msg.content), "USER": str(msg.sender_username), "TIME" : str(msg.time)}
                            json_data = json.dumps(data).encode('utf-8')
                            self.client.send(json_data + b'\n')          
                        current_users = self.database.get_users_in_lobby(self.current_lobby)
                        for user in current_users:
                            data = {'TYPE': 'USER', 'USERNAME':  str(user.username)}
                            json_data = json.dumps(data).encode('utf-8')
                            self.client.send(json_data + b'\n')  
                                            
                except Exception as e:
                    # Handle exceptions (e.g., client disconnects)
                    print(f"Error Type: {type(e).__name__}")
                    print(f"Error Info: {e}")
                    break
        print(f'Disconnected with {str(self.address)}')
            
    def broadcast(self, message, time):
        # Broadcast a message to all clients in the current lobby
        data = {'TYPE' : 'MESSAGE', 'CONTENT' : message, "USER" : self.nickname, "TIME": time}
        for client in self.clientDict[self.current_lobby]:
            json_data = json.dumps(data).encode('utf-8')
            client.send(json_data)
