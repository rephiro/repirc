#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, string
import time
import argparse
import threading
import sys

class Bot(threading.Thread):

	def __init__(self, host, port, nick, channel,
			charset='utf-8',
			username='papabot',
			realname='papabot',
			hostname='bot',
			servername='bot'):
		super(Bot, self).__init__()
		self.setDaemon(True)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = host
		self.port = port
		self.nick = nick
		self.channel = channel
		self.username = username
		self.realname = realname
		self.hostname = hostname
		self.servername = servername
		self.charset = charset
		self.logfile = open('/tmp/log.txt', 'a+')

	def connect(self):
		self.sock.connect((self.host, self.port))

	def login(self):
		self.send("USER %s %s %s %s" % \
			(self.username, self.hostname, self.servername, self.realname))
		self.send("NICK " + self.nick)

	def join(self):
		self.send("JOIN %s" % self.channel)

	def send(self, command):
		self.sock.send(command + '\n')

	def msg(self, msg):
		msg = msg.encode(self.charset)
		str = "PRIVMSG {channel} {msg}\n".format(channel=self.channel, msg=msg)
		self.sock.send(str)
		self.log("(my_msg) " + str)

	def log(self, txt):
		# TODO: 日時追加
		txt = txt.rstrip("\n")
		print txt
		txt = txt + "\n"
		self.logfile.write(txt)
		self.logfile.flush()

	def msg_bot(self, msg):
		nickname = msg[0].lstrip(":").split("@")[0].split("!")[0]
		username = msg[0].lstrip(":").split("@")[0].split("!")[1]
		client = msg[0].lstrip(":").split("@")[1]
		channel = msg[2]
		terms = " ".join(msg[3:]).decode(self.charset).lstrip(":").rstrip("\n")

		# ここにbotロジックを追加していく #
		# (プラグイン化できたらいいなぁ)  # 

		if terms.find("bot") >= 0:
			self.msg(u"私がbotだ。")

		###################################

	def recv(self):
		buffer = self.sock.recv(1024)
		self.log(buffer)
		msg = string.split(buffer.rstrip("\n"))
		msg = buffer.split(" ")
		if msg[0] == "PING":
			self.send("PONG %s" % msg[1])
		if msg[1] == 'PRIVMSG':
			self.msg_bot(msg)

	def run(self):

		self.log("charset: {charset}".format(charset=self.charset))
		self.connect()
		self.login()
		self.log("server logined.")

		# TODO:いずれsleepじゃない方法になおす。
		time.sleep(10)

		self.join()
		self.log("channel joinned.")
		self.log("started recieving message...")
		while (1):
			self.recv()

	def stop(self):
		self.sock.close()

def main():
	parser = argparse.ArgumentParser(description="IRC Bot")
	parser.add_argument("-s", "--server",
		type=str,
		metavar="<address>",
		default="172.20.150.201",
		help="IRC server IP address")
	parser.add_argument("-p", "--port",
		type=int,
		metavar="<port>",
		default=6667,
		help="IRC server port num")
	parser.add_argument("-n", "--nickname",
		type=str,
		metavar="<nickname>",
		default="papabot",
		help="Login nick name")
	parser.add_argument("-c", "--channel",
		type=str,
		metavar="<channel>",
		default="#nfv",
		help="Login channel name")
	parser.add_argument("-e", "--charset",
		type=str,
		metavar="<charset>",
		default="utf-8",
		help="Server charset(default: utf-8)")
	args = parser.parse_args()

	bot = Bot(args.server, args.port, args.nickname, args.channel, charset=args.charset)
	bot.start()
	while True:
		line = sys.stdin.readline()
		bot.msg(line.rstrip("\n").decode('utf-8'))

if __name__ == '__main__':
	main()

