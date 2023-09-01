
import json
from .manager import Manager


class Client:
    
    def __init__(self, client, address, clientDict, database):
        self.client = client
        self.nickname = None
        self.address = address
        self.clientDict = clientDict
        self.database : Manager = database 
        self.current_lobby = "lobby0"
        
        
    def handler(self):
        
        data = {'TYPE' : 'USERNAME'}
        json_data = json.dumps(data).encode('utf-8')
        self.client.send(json_data)
        
        received_object = self.client.recv(1024).decode('utf-8')
        username_message = json.loads(received_object)
        
        if username_message['TYPE'] != "QUIT":
            self.nickname : str = username_message["TYPE"]
        
            self.clientDict["lobby0"].append(self.client)
            if self.database.create_user(self.nickname) == True:
                self.database.add_user_to_lobby(self.nickname, "lobby0")
            
            data = {'TYPE' : 'VALIDATED'}
            json_data = json.dumps(data).encode('utf-8')
            self.client.send(json_data)

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
                        self.broadcast(message["CONTENT"], message["TIME"])
                        self.database.create_message(message["CONTENT"], message["LOBBY"], self.nickname, message["TIME"])
                    elif message['TYPE'] == "QUIT":
                        for key in self.clientDict:
                            self.clientDict[key] = [item for item in self.clientDict[key] if item != self.client]
                        self.client.close()
                        break
                    elif message['TYPE'] == "CHANGE_LOBBY":
                        self.clientDict[self.current_lobby].remove(self.client)
                        self.current_lobby = message["LOBBY"]
                        self.clientDict[self.current_lobby].append(self.client)
                        self.database.add_user_to_lobby(self.nickname, self.current_lobby)
                        
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
                    print(f"Error Type: {type(e).__name__}")
                    print(f"Error Info: {e}")
                    break
        print(f'Disconnected with {str(self.address)}')
            
    def broadcast(self, message, time):
        data = {'TYPE' : 'MESSAGE', 'CONTENT' : message, "USER" : self.nickname, "TIME":time}
        for client in self.clientDict[self.current_lobby]:
            json_data = json.dumps(data).encode('utf-8')
            client.send(json_data)