import editdatabase

class Main:
    """Manage playeraktivies on servers"""
    def __init__(self):
        self.dbmanger = editdatabase.Databasemanager()

    def main(self, ctx, cmd=None, message=None):
        """main class to control diffrent commands"""
        if cmd == "add":
            self.add(ctx, message)
        elif cmd == "list":
            self.listwatchserver(ctx)
        elif cmd.split("")[0] == "details":
            self.details(cmd, ctx)

    async def add(self, ctx, message):
        """add a new server to the database which is gona be watched"""
        self.dbmanger.plyhistoryadd(message)
        await ctx.channel.send("added server")

    def listwatchserver(self, ctx):
        """list all servers which are being watched"""
        pass

    def details(self, message, ctx):
        """print all player activities which are logged in the database"""
        pass
