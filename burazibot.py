#!/usr/bin/python

from jabby.jabberbot import JabberBot, botcmd
import datetime
import os
from ConfigParser import SafeConfigParser
import pickle


class SystemInfoJabberBot(JabberBot):
    @botcmd
    def printhistory(self, mess, args):
        """print history up to x last lines (default 10)"""
        try:
            lines = -1 * int(args)
        except:
            lines = -10
        return "\n" + "\n".join(self.history[lines:])

    @botcmd
    def gettags(self, mess, args):
        """print stuff taged with tag"""
        if args in self.tags:
            return "\n" + "\n".join(self.tags[args])
        else:
            return "Nema nis buraz!"

    @botcmd
    def infotags(self, mess, args):
        """Returns tags that are currently in use"""
        return "\n" + " ".join(self.tags.keys())

    @botcmd
    def serverinfo(self, mess, args):
        """Displays information about the server"""
        version = open('/proc/version').read().strip()
        loadavg = open('/proc/loadavg').read().strip()

        return '%s\n\n%s' % (version, loadavg, )

    @botcmd
    def getservertime(self, mess, args):
        """Displays current server time"""
        return str(datetime.datetime.now())

    @botcmd
    def rot13(self, mess, args):
        """Returns passed arguments rot13'ed"""
        return args.encode('rot13')

    @botcmd
    def whoami(self, mess, args):
        """Tells you your username"""
        return mess.getFrom().getStripped()

    @botcmd
    def writehistfile(self, mess, args):
        """Writes the history/tags to the disk"""
        try:
            f = open(self.histfile, "w")
            pickle.dump((self.history, self.tags), f)
            f.close()
            return "Fajl snimljen buraz!"
        except IOError:
            self.log.info("No history/tags file available")
            return "Niman di da sniman, e!"

    def shutdown(self):
        self.writehistfile("", "")
        pass

if __name__ == "__main__":

    conf = SafeConfigParser()
    conf.read("./vars.ini")

    if conf.get("tls", "enabled") != "":
        secure = int(conf.get("tls", "enabled"))

    bot = SystemInfoJabberBot(conf.get("xmpp", "username"),
                              conf.get("xmpp", "pass"),
                              histfile=conf.get("local", "histfile"),
                              secure=secure,
                              debug=False)
    bot.join_room(conf.get("xmpp", "room"))
    bot.serve_forever()
