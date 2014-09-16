#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
IRC ボットです。
config.ini ファイルから必要な設定を読み込んで使用します
"""

import irc.bot
import irc.strings
import datetime
import codecs
from irc.connection import Factory
from ConfigParser import SafeConfigParser

# 設定ファイル読み込み
config = SafeConfigParser()
config.read('/home/user/irc/new_config.ini')
IRC_SERVER = str(config.get("IRC", "SERVER"))
IRC_PORT = int(config.get("IRC", "PORT"))
IRC_NICK = str(config.get("IRC", "NICK"))
IRC_PASS = str(config.get("IRC", "PASS"))
IRC_CHANNELS = str(config.get("IRC", "CHANNELS")).split(" ")
IRC_TIMER_SEC = int(config.get("IRC", "TIMER_SEC"))
if int(config.get("IRC", "SSL")):
    IRC_SSL = True
else:
    IRC_SSL = False
LOG_DIR = str(config.get("LOG", "LOG_DIR"))


class IRC_Bot(irc.bot.SingleServerIRCBot):
    """
    IRC ボットクラス
    """

    def __init__(self, server, port, nickname, password=None, ssl=False):
        """
        初期化処理
        """
        server_obj = irc.bot.ServerSpec(server, port, password)
        connection_factory = Factory()
        if ssl:
            connection_factory.from_legacy_params(ssl=True)
        irc.bot.SingleServerIRCBot.__init__(self, [server_obj], nickname, nickname, 60, connect_factory=connection_factory)
        self.channel = IRC_CHANNELS
        self.queue = []

    def on_nicknameinuse(self, c, e):
        """
        ニックネームが既に使われていたときの処理
        """
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        """
        サーバにログインしたときの処理
        """
        for item in self.channel:
            c.join(item)

    def on_privmsg(self, c, e):
        """
        プライベートメッセージを受信したときの処理
        """
        self.do_command(e, e.arguments[0])
        post_time = datetime.datetime.now()
	input_data = "%s:%s %s > %s\n" % (post_time.strftime("%2H"), post_time.strftime("%2M"), e.source.split("!")[0], e.arguments[0])
	if str(e.source.split("!")[0]) == c.nick:
            log_write(e.target, input_data)
	else:
            log_write(e.source.split("!")[0], input_data)

    def on_privnotice(self, c, e):
        """
        プライベートメッセージを受信したときの処理
        """
        post_time = datetime.datetime.now()
	input_data = "%s:%s %s > %s\n" % (post_time.strftime("%2H"), post_time.strftime("%2M"), e.source.split("!")[0], e.arguments[0])
	if str(e.source.split("!")[0]) == c.nick:
            log_write(e.target, input_data)
	else:
            log_write(e.source.split("!")[0], input_data)


    def on_pubmsg(self, c, e):
        """
        チャンネルにメッセージを受信したときの処理
        """
        post_time = datetime.datetime.now()
	input_data = "%s:%s %s > %s\n" % (post_time.strftime("%2H"), post_time.strftime("%2M"), e.source.split("!")[0], e.arguments[0])
        channel_data = e.target.replace("#", "")
	#log_write(e.target.replace("#", ""), input_data)
	log_write(channel_data, input_data)
        if channel_data != IRC_SERVER:
            log_write2(channel_data, input_data)

    def on_pubnotice(self, c, e):
        """
        notice(接続しているチャンネル)を受信したときの処理
        """
        post_time = datetime.datetime.now()
	input_data = "%s:%s %s > %s\n" % (post_time.strftime("%2H"), post_time.strftime("%2M"), e.source.split("!")[0], e.arguments[0])
        channel_data = e.target.replace("#", "")
	#log_write(e.target.replace("#", ""), input_data)
	log_write(channel_data, input_data)
        if channel_data != IRC_SERVER:
            log_write2(channel_data, input_data)

#    def privmsg(self, target, msg):
#        """
#        メッセージ送信
#        """
#        if target in self.channel:
#            self.connection.privmsg(target, msg.encode("iso-2022-jp", "ignore"))
#        else:
#            post_time = datetime.datetime.now()
#            self.connection.privmsg(target, msg.encode("iso-2022-jp", "ignore"))
#            input_date = "%s:%s %s > %s\n" % (post_time.strftime("%2H"), post_time.strftime("%2M"), self._nickname, msg.encode('utf-8'))
#            log_write(target, input_date)

    def do_command(self, e, cmd):
        """
        独自定義のコマンド
        """
        nick = e.source.nick
        c = self.connection

        if cmd == "disconnect":
            self.disconnect()
        elif cmd == "die":
            self.die()
        elif cmd == "stats":
            for chname, chobj in self.channels.items():
                c.notice(nick, "--- Channel statistics ---")
                c.notice(nick, "Channel: " + chname)
                users = chobj.users()
                users.sort()
                c.notice(nick, "Users: " + ", ".join(users))
                opers = chobj.opers()
                opers.sort()
                c.notice(nick, "Opers: " + ", ".join(opers))
            c.notice(nick, "--------------------------")
        else:
            pass

    def add_execute_delayed(self, sec, callback, obj):
        """
        遅延実行関数（指定秒たったら、指定関数を実行）
        """
        self.ircobj.execute_delayed(sec, callback, obj)


def call_timer(bot):
    """
    タイマー関数
    この中で定期的に実行する操作を定義
    """
    bot.add_execute_delayed(IRC_TIMER_SEC, call_timer, (bot,))


def log_write(TChannel, input_data):
    """
    ログの書き込み処理
    """
    d = datetime.datetime.today()
    logname = LOG_DIR + TChannel + "_" + d.strftime("%Y%m%d") + ".log"
    logfile = codecs.open(logname, "a", "utf-8")
    logfile.write(input_data.decode('shift-jis').encode('utf-8'))
    logfile.close()

def log_write2(TChannel, input_data):
    logname = LOG_DIR + u"irc.log"
    logfile = codecs.open(logname, "a", "utf-8")
    logfile.write(TChannel.encode('utf-8') + u":" + input_data.decode('shift-jis').encode('utf-8'))
    logfile.close()


def main():
    bot = IRC_Bot(IRC_SERVER, IRC_PORT, IRC_NICK, IRC_PASS, IRC_SSL)
    bot.add_execute_delayed(IRC_TIMER_SEC, call_timer, (bot,))
    bot.start()

if __name__ == "__main__":
    main()
