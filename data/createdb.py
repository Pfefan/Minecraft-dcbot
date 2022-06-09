"""module imports"""
import datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Watchserverip(Base):
    """creating Server"""

    __tablename__ = "watchhostnames"

    id = Column(String, primary_key=True)

class Watchserverinfo(Base):
    """creating Server"""

    __tablename__ = "watchinfo"

    id = Column(Integer, primary_key=True)
    hostname = Column(String, ForeignKey("watchhostnames.id"))
    onplayer = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)

class Onlineserver(Base):
    """creating Server"""

    __tablename__ = "onlineservers"

    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    version = Column(String)
    onplayer = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)

class Defaultserver(Base):
    """creating Server"""

    __tablename__ = "defaultdatabase"

    server_id = Column(Integer, primary_key=True)
    server_hostname = Column(String)
