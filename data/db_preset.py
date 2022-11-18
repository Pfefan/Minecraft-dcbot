"""module imports"""
import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base

defaultbase = declarative_base()
dbbase = declarative_base()

class Watchserverip(dbbase):
    """creating Server"""

    __tablename__ = "watchhostnames"

    id = Column(String, primary_key=True)

class Watchserverinfo(dbbase):
    """creating Server"""

    __tablename__ = "watchinfo"

    id = Column(Integer, primary_key=True)
    onplayer = Column(Integer)
    hostname = Column(String, ForeignKey("watchhostnames.id"),
                      nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)

class Onlineserver(dbbase):
    """creating Server"""

    __tablename__ = "onlineservers"

    id = Column(Integer, primary_key=True)
    hostname = Column(String)
    version = Column(String)
    onplayer = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.now)

class Defaultserver(defaultbase):
    """creating Server"""

    __tablename__ = "server"

    server_id = Column(Integer, primary_key=True)
    server_hostname = Column(String)
