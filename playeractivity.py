
class Main:
    """Manage playeraktivies on servers"""
    def __init__(self):
        pass

    def main(self, ctx, message=None):
        """main class to control diffrent commands"""
        if message == "add":
            self.add(ctx)
        elif message == "list":
            self.listwatchserver(ctx)
        elif message.split("")[0] == "details":
            self.details(message, ctx)

    def add(self, ctx):
        """add a new server to the database which is gona be watched"""
        pass

    def listwatchserver(self, ctx):
        """list all servers which are being watched"""
        pass

    def details(self, message, ctx):
        """print all player activities which are logged in the database"""
        pass
