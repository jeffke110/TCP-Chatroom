from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .database import User, Message, Lobby, LobbyUser, Base

class Manager:
    def __init__(self, database_url):
        # Initialize the manager with a database URL.
        self.engine = create_engine(database_url)
        # Create tables if they don't exist.
        Base.metadata.create_all(self.engine)
        # Create a session for database operations.
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def create_user(self, username):
        # Create a new user if the username doesn't already exist.
        user = self.session.query(User).filter_by(username=username).first()
        if user is None:
            self.session.add(User(username=username))
            self.session.commit()
            return True  # User created successfully
        else:
            return False  # User already exists

    def create_lobby(self, name):
        # Create a new lobby if the name doesn't already exist.
        lobby = self.session.query(Lobby).filter_by(name=name).first()
        if lobby is None:
            self.session.add(Lobby(name=name))
            self.session.commit()
            return True  # Lobby created successfully
        else:
            return False  # Lobby already exists

    def add_user_to_lobby(self, username, lobby_name):
        # Add a user to a lobby.
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
        # Create a new message and associate it with a lobby and user.
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            message = Message(content=content, lobby_name=lobby_name, sender_username=username, time=time)
            self.session.add(message)
            lobby.messages.append(message)
            self.session.commit()
            return True  # Message created successfully
        else:
            return False  # Lobby not found

    def remove_user_from_lobby(self, user, lobby_name):
        # Remove a user from a lobby.
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            lobby.users.remove(user)
            self.session.commit()
            return True  # User removed from lobby successfully
        else:
            return False  # Lobby not found

    def get_users_in_lobby(self, lobby_name):
        # Get a list of users in a lobby.
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            return lobby.users
        else:
            return False  # Lobby not found

    def get_messages_in_lobby(self, lobby_name):
        # Get a list of messages in a lobby.
        lobby = self.session.query(Lobby).filter_by(name=lobby_name).first()
        if lobby:
            return lobby.messages
        else:
            return False  # Lobby not found

    def close(self):
        # Close the database session.
        self.session.close()
