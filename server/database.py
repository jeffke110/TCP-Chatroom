from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for SQLAlchemy models
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column("username", String)
    
    def __repr__(self):
        return f'{self.username}'

class Message(Base):
    __tablename__ = "messages"
    id = Column("id", Integer, primary_key=True)
    content = Column("content", String)
    time = Column("time", String)
    lobby_name = Column("lobby_name", String, ForeignKey("lobbies.name"))
    sender_username = Column("sender_username", String, ForeignKey("users.username"))
    
class Lobby(Base):
    __tablename__ = "lobbies"
    id = Column(Integer, primary_key=True)
    name = Column("name", String)
    # Establish a many-to-many relationship between lobbies and users
    users = relationship("User", secondary="lobby_users")
    messages = relationship("Message", backref="lobby")

class LobbyUser(Base):
    __tablename__ = "lobby_users"
    # Define a composite primary key to link users and lobbies
    lobby_name = Column("lobby_name", String, ForeignKey("lobbies.name"), primary_key=True)
    username = Column("username", String, ForeignKey("users.username"), primary_key=True)
