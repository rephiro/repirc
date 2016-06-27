#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket, string
import time
import argparse
import threading
import sys

class Bot(threading.Thread):

	def __init__(self, host, port, nick, channel, username='papabot', realname='papabot', hostname='bot', servername='bot'):
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
		#self.sock.send("PRIVMSG " + self.channel + " " + msg + '\n')
		str = "PRIVMSG {channel} {msg}\n".format(channel=self.channel, msg=msg)
		self.sock.send(str)
		self.log("(my_msg) " + str)

	def log(self, txt):
		self.logfile.write(txt)
		self.logfile.flush()

	def recv(self):
		buffer = self.sock.recv(1024)
		self.log(buffer)
		msg = string.split(buffer.rstrip("\n"))
		msg = buffer.split(" ")
		if msg[0] == "PING":
			self.send("PONG %s" % msg[1])
		if msg[1] == 'PRIVMSG':
			nickname = msg[0].lstrip(":").split("@")[0].split("!")[0]
			username = msg[0].lstrip(":").split("@")[0].split("!")[1]
			client = msg[0].lstrip(":").split("@")[1]
			channel = msg[2]
			terms = " ".join(msg[3:]).lstrip(":").rstrip("\n")
			print "{nick}({user}) by {client}:{ch}:{terms}".format( \
				nick=nickname,
				user=username,
				client=client,
				ch=channel,
				terms=terms)

	def run(self):

		self.connect()
		self.login()
		print "server logined."
		time.sleep(3)
		self.join()
		print "channel joinned."
		print "started recieving message..."
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
	args = parser.parse_args()

	bot = Bot(args.server, args.port, args.nickname, args.channel)
	bot.start()
	while True:
		line = sys.stdin.readline()
		bot.msg(line.rstrip("\n"))

if __name__ == '__main__':
	main()
