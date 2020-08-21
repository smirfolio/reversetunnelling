#!/usr/bin/python

import time, datetime
import subprocess
import configparser
import telepot
from telepot.loop import MessageLoop

config = configparser.ConfigParser()
config.read('example.ini')
server = config['DEFAULT']['server']
user = config['DEFAULT']['user']
port = config['DEFAULT']['port']
timeout = config['DEFAULT']['timeout']
botkey = config['DEFAULT']['botkey']

def action(msg):
    chat_id = msg['chat']['id']
    username = msg['chat']['first_name']
    command = msg['text']
#    print ('Received Chat id : %s' % chat_id)
    message = ''
    if chat_id == 896653533:
        if 'Ssh' in command:
            if 'run' in command:
                message = 'Start tunnelling'
                subprocess.call("./ssh_tunnel.sh " + server + " " + user + " " + port + " " + timeout, shell=True)
            if 'stop' in command:
                message = 'Stop tunnelling'
                subprocess.call("./stop_tunnelling.sh", shell=True)
            telegram_bot.sendMessage (chat_id, message)
#       print ('Received From : %s' % username)
#       print ('Received: %s' % command)
telegram_bot = telepot.Bot(botkey)
#print (telegram_bot.getMe())
MessageLoop(telegram_bot, action).run_as_thread()
#print ('Up and Running....')

while 1:
    time.sleep(10)
