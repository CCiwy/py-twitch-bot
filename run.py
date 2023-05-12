#!/usr/bin/env python
#-*- coding: utf-8

__AUTHOR__ =  'Quesnok'
__LICENSE__ = 'MIT'
__DOC__ = 'Twitch Bot written in python, developed live on stream'

# Import Built-Ins
import os

# Import Home-Grown
from src.app import App       



# TWITCH AUTH DATA
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN', False)
NICK = os.getenv('NICK', False)
CLIENT_SECRET = os.getenv('CLIENT_SECRET', False)
CLIENT_ID = os.getenv('CLIENT_ID', False)
CHANNEL = os.getenv('CHANNEL', False)
 

def main():
    app = App(NICK,
            ACCESS_TOKEN,
            CHANNEL
        )

    app.start()
    while True:
        try:
            app.run()
        except KeyboardInterrupt:
            app.exit()
            exit(0)


if __name__ == '__main__':
    main()
