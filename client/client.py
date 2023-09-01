import socket
import threading
import logging
import random
import json
from .gui import Gui
from tkinter import *
from tkinter import ttk
from datetime import datetime

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.nickname = None
        self.app : Gui = None
        self.running = True
        self.current_lobby = "lobby0"
        self.update = False

    def connect_to_server(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_ip, self.server_port))
        print("Connected to server.")
        
    def receive_messages(self):
        while self.running:
            try:
                received_object = self.client_socket.recv(4096).decode('utf-8')
                payloads = received_object.strip().split('\n')
                for payload in payloads:
                    message = json.loads(payload)
                    if message['TYPE'] == "USERNAME":
                        self.app.register_button.config(command=self.send_login)
                    elif message['TYPE'] == "VALIDATED":
                        self.app.create_widgets()
                        self.app.nickname_label.config(text=self.nickname)
                        self.write_thread = threading.Thread(target=self.write_messages)
                        self.write_thread.start()
                    elif message['TYPE'] == "USER":
                        self.update = True
                        self.app.users.append(f"{message['USERNAME']}")
                    elif message['TYPE'] == "MESSAGE":
                        self.update = True
                        self.app.messages.append(message)
                if self.update:
                    self.app.update_users()
                    self.app.update_messages()
                    self.update = False
            except ConnectionAbortedError:
                pass
            except Exception as e:
                print(f"Error Type: {type(e).__name__}")
                print(f"Error Info: {e}")
                break

        
    def write_messages(self):
        self.app.send_button.config(command=self.send_message)
        self.app.message_entry.bind("<Return>", lambda event: self.send_message())  
        for index, lobby in enumerate(self.app.lobbies):
            lobby.config(command=lambda i=index: self.change_lobby(i))
            
    def send_login(self):
        if len(self.app.username_entry.get()) > 0:
            self.nickname = self.app.username_entry.get()
            data = {"TYPE" : self.nickname}
            json_data = json.dumps(data).encode('utf-8')
            self.client_socket.send(json_data)

    def change_lobby(self, index):
    
        self.app.lobbies[index].config(bg="white")
        for row, lobby in enumerate(self.app.lobbies):
            if index is not row:
                lobby.config(bg="grey1")  
        self.app.users = []
        self.app.messages = []
        self.current_lobby = f'lobby{index}'      
        data = {"TYPE": "CHANGE_LOBBY", "LOBBY" : f'lobby{index}'}
        json_data = json.dumps(data).encode('utf-8')
        self.client_socket.send(json_data)
        
    def send_message(self):
        info = self.app.message_entry.get()
        if(len(info) > 0):
            self.app.message_entry.delete(0, len(info))
            current_time = datetime.now()
            formatted_time = current_time.strftime("%I:%M%p %m/%d/%y")
            data = {"TYPE" :"MESSAGE", "CONTENT" : info, "TIME": formatted_time, "LOBBY" : self.current_lobby}
            json_data = json.dumps(data).encode('utf-8')
            self.client_socket.send(json_data)

    def quit(self):
        self.running = False
        print("Disconnected from server.")
        data = {"TYPE" : "QUIT"}
        json_data = json.dumps(data).encode('utf-8')
        self.client_socket.send(json_data)
        self.client_socket.close()
        self.app.root.destroy()
        
    def start(self):
        root = Tk()
        self.app = Gui(root)
        self.app.root.protocol('WM_DELETE_WINDOW', self.quit)
        self.connect_to_server()
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.start()
        root.mainloop()
        