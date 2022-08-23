"""module imports"""
import sqlalchemy
from data.createdb import defaultbase, dbbase
from data.createdb import Onlineserver, Watchserverinfo, Watchserverip, Defaultserver

class Databasemanager():
    """Databasemanage"""

    def __init__(self) -> None:
        """init func"""
        db_servers = sqlalchemy.create_engine("sqlite:///data/servers.db")
        defaultbase.metadata.create_all(db_servers)
        self.session_servers = sqlalchemy.orm.sessionmaker()
        self.session_servers.configure(bind=db_servers)

        db_database = sqlalchemy.create_engine("sqlite:///data/database.db")
        dbbase.metadata.create_all(db_database)
        self.session_database = sqlalchemy.orm.sessionmaker()
        self.session_database.configure(bind=db_database)

    def get(self, primary_key):
        """returns a specific id out of the database"""
        with self.session_servers() as session:
            return session.query(Defaultserver).get(primary_key).server_hostname

    def lengh(self):
        """returns the lengh of the database"""
        with self.session_servers() as session:
            return session.query(Defaultserver).count()

    def all(self):
        """returns all hostnames entries of the database"""
        hostnames = []
        with self.session_servers() as session:
            database = session.query(Defaultserver).all()
            for i in database:
                hostnames.append(i.server_hostname)
            return hostnames

    def onserverssave(self, data):
        """saves online servers to a history database
         and then it adds the new entries to the online database"""
        with self.session_database() as session:
            session.query(Onlineserver).delete()
            session.commit()

        with self.session_database() as session:
            for i in data:
                onserverdb = Onlineserver(hostname=i[0], version=i[1], onplayer=i[2])
                session.add(onserverdb)
            session.commit()

    def onserversget(self):
        """returns all entries of database """
        serverinfo = []
        with self.session_database() as session:
            database = session.query(Onlineserver).all()
            for i in database:
                serverinfo.append((i.hostname, i.version, i.onplayer, i.timestamp))
            return serverinfo

    def plyhistoryadd(self, data):
        """saves a new History entry into database"""
        with self.session_database() as session:
            entry = Watchserverip(id=data)
            session.add(entry)
            session.commit()

    def plyhistoryall(self):
        """returns all entries saved in database"""
        entries = []
        with self.session_database() as session:
            database = session.query(Watchserverip).all()
            for i in database:
                entries.append(i.id)
            return entries

    def plyhistoryremove(self, data):
        """removes a specific entry from database"""
        with self.session_database() as session:
            session.query(Watchserverip).filter(Watchserverip.id == data).delete()
            session.query(Watchserverinfo).filter(Watchserverinfo.hostname == data).delete()
            session.commit()


    def plyhistoryinfosave(self, _hostname, _players):
        """saves info for a certain server"""
        with self.session_database() as session:
            entry = Watchserverinfo(hostname = _hostname, onplayer=_players)
            session.add(entry)
            session.commit()

    def plyhistoryinfoget(self, _hostname):
        """returns info for a certain server"""
        entries = []
        with self.session_database() as session:
            database = session.query(Watchserverinfo) \
                              .filter(Watchserverinfo.hostname == _hostname).all()
            for i in database:
                entries.append((i.onplayer, i.hostname, i.timestamp))
        return entries

    def plyhistorygettime(self):
        """returns all entries with timestamp"""
        entries = []
        with self.session_database() as session:
            database = session.query(Watchserverinfo).all()
            for i in database:
                entries.append((i.id, i.timestamp))
        return entries

    def plyhistoryautodel(self, data):
        """deletes to old entries"""
        with self.session_database() as session:
            session.query(Watchserverinfo).filter(Watchserverinfo.id == data).delete()
            session.commit()
