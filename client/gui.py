from tkinter import *
from tkinter import ttk, font

class Gui:
    def __init__(self, root : Tk):
        self.root = root
        self.root.geometry("1200x800")
        self.root.minsize(width=1200, height=800)
        self.root.maxsize(width=1200, height=800)
        self.root.title("Chat App")
        self.primary_color = "grey6"
        self.secondary_color = "grey1"
        self.font_color = "red3"
        self.messages = []
        self.lobbies = []
        self.users = []
        self.primary_font = font.Font(family="Inter Light", size=12, weight="bold")
        self.lobby_font = font.Font(family="Inter Light", size=7, weight="bold")
        self.message_font = font.Font(family="Inter Light", size=9, weight="bold")
        self.user_font = font.Font(family="Inter Light", size=9, weight="bold")
        self.entry_font = font.Font(family="Inter Light", size=12)
        self.create_widgets()
        
    
    def create_lobbies(self):
        main_frame = Frame(self.root)
        main_frame.grid(row=2, column=0, rowspan=8, columnspan=1, sticky="nsew")
        self.lobby_canvas = Canvas(main_frame, width=150)
        self.lobby_canvas.pack(side=LEFT, fill=BOTH, expand=1)
        lobby_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.lobby_canvas.yview)
        lobby_scrollbar.pack(side=RIGHT, fill=Y)
        self.lobby_canvas.configure(yscrollcommand=lobby_scrollbar.set)
        self.lobby_frame = Frame(self.lobby_canvas, background=self.secondary_color)
        self.lobby_canvas.create_window((0,0), window=self.lobby_frame, anchor="nw")

        for lobby in range(10):
            if lobby is 0:
                self.a_lobby = Button(self.lobby_frame, text=f'Lobby {lobby}', width=20, height=2, background="white", foreground=self.font_color, font=self.lobby_font)
            else:
                self.a_lobby = Button(self.lobby_frame, text=f'Lobby {lobby}', width=20, height=2, background=self.secondary_color, foreground=self.font_color, font=self.lobby_font)
            self.a_lobby.grid(row=lobby, column=0, pady=10, padx=30)
            self.lobbies.append(self.a_lobby)
            
        self.lobby_frame.update_idletasks()
        self.lobby_canvas.configure(scrollregion=self.lobby_canvas.bbox("all"), background=self.secondary_color)
            
    def create_mesages(self):
        main_frame = Frame(self.root, background=self.secondary_color)
        main_frame.grid(row=1, column=2, rowspan=9, columnspan=1, sticky="nsew")

        self.message_canvas = Canvas(main_frame, width=500, bg=self.secondary_color, )
        self.message_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        message_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.message_canvas.yview)
        message_scrollbar.pack(side=RIGHT, fill=Y)

        self.message_canvas.configure(yscrollcommand=message_scrollbar.set)

        self.message_frame = Frame(self.message_canvas, background=self.secondary_color)
        self.message_canvas.create_window((0, 0), window=self.message_frame, anchor="sw")

    
    def update_messages(self):
        for widget in self.message_frame.winfo_children():
            widget.destroy()
        
        for row, message in enumerate(self.messages):
            #Label(self.message_frame, text=f'{message}', width=75, height=1, anchor="w", background=self.secondary_color, foreground=self.font_color, font=self.message_font).grid(row=row, column=0, pady=10, padx=10)
            username_label = ttk.Label(self.message_frame, text=f"{message['USER']}:", background=self.secondary_color, foreground=self.font_color, font=self.message_font, wraplength=60)  # Adjust the wraplength value as needed
            username_label.grid(row=row, column=0, sticky="w", padx=10, pady=5)

            message_label = ttk.Label(self.message_frame, text=f"{message['CONTENT']}", background=self.secondary_color, foreground="white", font=self.message_font, wraplength=450)  # Adjust the wraplength value as needed
            message_label.grid(row=row, column=1, sticky="w", padx=10, pady=5)

            time_label = ttk.Label(self.message_frame, text=f"{message['TIME']}", background=self.secondary_color, foreground="orange", font=self.message_font)
            time_label.grid(row=row, column=2, sticky="w", padx=10, pady=5)

        self.message_frame.update_idletasks()
        self.message_canvas.configure(scrollregion=self.message_canvas.bbox("all"))
        
        

    def create_users(self):
        main_frame = Frame(self.root)
        main_frame.grid(row=1, column=4, rowspan=11, columnspan=1, sticky="nsew")
            
        self.users_canvas = Canvas(main_frame, width=200, bg=self.secondary_color)
        self.users_canvas.pack(side=LEFT, fill=BOTH, expand=1)
            
        users_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=self.users_canvas.yview)
        users_scrollbar.pack(side=RIGHT, fill=Y)

        self.users_canvas.configure(yscrollcommand=users_scrollbar.set)
        
        self.users_frame = Frame(self.users_canvas,  background=self.secondary_color)
        self.users_canvas.create_window((0, 0), window=self.users_frame, anchor="nw")

    def update_users(self):
        for widget in self.users_frame.winfo_children():
            widget.destroy()

        for row, user in enumerate(self.users):
            Label(self.users_frame, text=f'{user}', width=34, height=1, anchor="w", wraplength=200, background=self.secondary_color, foreground=self.font_color, font=self.user_font).grid(row=row, column=0, pady=10, padx=10)

        self.users_frame.update_idletasks()
        self.users_canvas.configure(scrollregion=self.users_canvas.bbox("all"))


    def create_widgets(self):
        self.root.config(bg=self.primary_color)
        
        self.nickname_label = Label(self.root, text="Nickname:", background=self.primary_color, foreground=self.font_color, font=self.primary_font)
        self.nickname_label.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")
        
        self.lobby_label = Label(self.root, text="Lobbies", background=self.primary_color, foreground=self.font_color, font=self.primary_font)
        self.lobby_label.grid(row=1, column=0, rowspan=1, columnspan=1, sticky="nsew")
        
        self.space_label = Label(self.root, text="", background=self.primary_color)
        self.space_label.grid(row=0, column=1, rowspan=11, columnspan=1, sticky="nsew")
        
        self.message_label = Label(self.root, text="Messages", background=self.primary_color, foreground=self.font_color, font=self.primary_font)
        self.message_label.grid(row=0, column=2, rowspan=1, columnspan=1, sticky="nsew")
        
        self.message_entry = Entry(self.root, width=75, background=self.secondary_color, foreground="white", font=self.entry_font)
        self.message_entry.grid(row=10, column=2, columnspan=1, sticky="w")

        
        self.send_button = Button(self.root, text="Send", width=10, height=1,background=self.secondary_color, foreground=self.font_color, font=self.user_font)
        self.send_button.grid(row=10, column=2, sticky="e", padx=15)
        
        self.space_label_two= Label(self.root, text="", background=self.primary_color)
        self.space_label_two.grid(row=0, column=3, rowspan=11, columnspan=1, sticky="nsew")
        
        self.user_label = Label(self.root, text="Users", background=self.primary_color, foreground=self.font_color, font=self.primary_font)
        self.user_label.grid(row=0, column=4, rowspan=1, columnspan=1, sticky="nsew")
        
        self.logout_button = Button(self.root, text="Logout", width=10, height=1, background=self.secondary_color, foreground=self.font_color, font=self.primary_font)
        self.logout_button.grid(row=10, column=0)
        
        self.create_lobbies()
        self.create_mesages()
        self.create_users()
        
        for row in range(11): 
            self.root.grid_rowconfigure(row, weight=1)
        for col in range(5): 
            self.root.grid_columnconfigure(col, weight=1)
