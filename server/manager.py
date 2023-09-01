from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import User, Message, Lobby, LobbyUser, Base

class Manager:
    def __init__(self, database_url):
        self.engine = create_engine(database_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_user(self, username):
        user = self.session.query(User).filter_by(username=username).first()
        if user is None:
            self.session.add(User(username=username))
            self.session.commit()
            return True
        else:
            return False

    def create_lobby(self, name):
        lobby = self.session.query(Lobby).filter_by(name=name).first()
        if lobby is None:
            self.session.add(Lobby(name=name))
            self.session.commit()
            return True
        else:
            return False

    def add_user_to_lobby(self, username, lobby_name):
        user = self.session.query(User).filter_by(username=username).first()
        if user:
            lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
            if lobby:
                if user in lobby.users:
                    return False  # User is already in the lobby
                else:
                    lobby.users.append(user)
                    self.session.commit()
                    return True  # Added user to lobby successfully
            else:
                return False  # Lobby not found
        else:
            return False  # User not found

    def create_message(self, content, lobby_name, username, time):
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            message = Message(content=content, lobby_name=lobby_name, sender_username=username, time=time)
            self.session.add(message)
            lobby.messages.append(message)
            self.session.commit()
            return True
        else:
            return False  # Lobby not found
       

    def add_message_to_lobby(self, message, lobby_name):
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            lobby.messages.append(message)
            self.session.commit()
            return True
        else:
            return False  # Lobby not found

    def remove_user_from_lobby(self, user, lobby_name):
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            lobby.users.remove(user)
            self.session.commit()
            return True
        else:
            return False  # Lobby not found

    def get_users_in_lobby(self, lobby_name):
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            return lobby.users
        else:
            return False


    def get_messages_in_lobby(self, lobby_name):
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            return lobby.messages
        else:
            return False

    def close(self):
        self.session.close()