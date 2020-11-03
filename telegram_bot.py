#!/usr/bin/python

import time, datetime
import subprocess
import configparser
import requests
import json
import random
import re
import telepot
from telepot.loop import MessageLoop

#
# Configuration parsed from the config.ini file, see README.md
#
config = configparser.ConfigParser()
config.read('config.ini')
server = config['DEFAULT']['server']
user = config['DEFAULT']['user']
port = config['DEFAULT']['port']
timeout = config['DEFAULT']['timeout']
botkey = config['DEFAULT']['botkey']
permitteduser_id = str(config['DEFAULT']['permitteduser_id'])

def getParameter(param, command):
    regex = r"(" + param + ":)([^,]+)"
    matches = re.search(regex, command, re.MULTILINE)
    return matches.group(2)

def action(msg):
    chat_id = str(msg['chat']['id'])
    username = msg['chat']['first_name']
    commandMessage = msg['text']
    message = "Nothing to say"

    #
    # Make a random quote to response to any message
    #
    try:
        quote_request = requests.get('https://type.fit/api/quotes')
    except:
        message = "Quotes .... well .... mmmm ...."
    else:
        if quote_request.status_code == 200:
            message = json.loads(quote_request.text)[random.randint(0,1640)]['text']

    # Check if the message come from authorized user
    if chat_id == permitteduser_id:
        #
        # Check for Ssh <action> in the message
        # Only 2 actions are permitted : `Ssh run` and `Ssh stop`
        #
        if 'Ssh' in commandMessage:
            # Check the action to perform
            if 'run' in commandMessage:
                # Check if a custom port is given on the message chat
                if 'port:' in commandMessage:
                    port = getParameter("port", commandMessage)
                    if 'server:' in commandMessage:
                        server = getParameter("server", commandMessage)

                ssh_command = "./tunnelling.sh " + server + " " + user + " " + port + " " + timeout + " && ./localProxy.sh"
                message = 'Start tunnelling on server ' + server

                # Run the tunneling script
                subprocess.call(ssh_command, shell=True)

            if 'stop' in commandMessage:
                if 'server:' in commandMessage:
                    server = getParameter("server", commandMessage)
                    ssh_command = "./stop_tunnelling.sh " + server
                    message = 'Stop tunnelling'
                    # Stop the tunnelling
                    subprocess.call(ssh_command, shell=True)

        telegram_bot.sendMessage (chat_id, message)


#
# Init the telegram bot
#
telegram_bot = telepot.Bot(botkey)
telegram_bot.sendMessage (permitteduser_id, "Yo ... I'm ready")
MessageLoop(telegram_bot, action).run_as_thread()

while 1:
    time.sleep(10)
