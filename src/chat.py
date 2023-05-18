# Import Built-Ins
from datetime import datetime as dt
from enum import Enum
from time import sleep

# import Home-Grown
from src.connection import Connection

from src.utils.logger import get_logger

class CommandAlreadyRegisterd(RuntimeError):
    def __init__(self, plugin_name, command):
        self.plugin_name = plugin_name
        self.command = command

    def __repr__(self):
        return f'{self.__class__.__name__} {self.plugin_name} {self.command}\n'


# IRC CHAT SERVER DATA
CHAT_ADDR = 'irc.chat.twitch.tv'
CHAT_PORT = 6667
CHAT_SERVER = (CHAT_ADDR, CHAT_PORT) 

# TWITCH IRC MARKER
MULTILINE_MARKER = '\r\n'
WELCOME_MSG = 'Welcome, GLHF!'


# capabilities
CAPS = ['commands', 'tags', 'membership']


class TwitchMessageType(str, Enum):
    """ make parsing of twitch message types easy"""
    PING = 'PING'
    JOIN = 'JOIN'
    PART = 'PART'
    PRIVMSG = 'PRIVMSG'
    CAP = 'CAP'
    ROOMSTATE = 'ROOMSTATE'
    USERSTATE = 'USERSTATE'

    def contains(self, other: str) -> bool:
        """
            takes in other: str , message recieved from twitch-chat via socket
        """
        return self.value in other


class Chat:
    def __init__(self, app, nick, oauth_token, channel):
        self.app = app
        self.errors = app.errors
        self.nick = nick
        self.oauth_token = oauth_token
        self.channel = channel

        self._connection = Connection(CHAT_SERVER)

        self.is_authenticated = self.authenticate()

        self._triggers = [] # store methods that get auto-triggerd by chat messages
        
        self.cap_commands = False
        self.cap_tags = False
       
        self.logger = get_logger('CHAT')
        self.running = False


        self._commands = {}
    # ----------------------- Properties -------------------
    @property
    def conn(self):
        if not self._connection.connected:
            self._connection.connect()
        return self._connection



    @property
    def timestamp(self):
        return f'[{dt.now().strftime("%H:%M:%S")}]'

    @property
    def plugins(self):
        return self.app.plugins

    

    # ----------------------- Start/Stop Handlers -------------------
    
    def start(self) -> None:
        """ on startup:
            load saves,
            send auth to twitch irc chat
        """ 
        if not self.is_authenticated:
            self.logger.error('not authenticated')
            return 
        self.join_channel()
        self.init_capabilities()

       
        self.running = True


    def exit(self) -> None:
        self.running = False



    def run(self) -> None:
        while self.running:
            msg = self.conn.receive()
            if msg:
                self.handle_msg(msg)
            sleep(1)
        self.logger.info('shutting down')


    ## ----------------------- Twitch Connection stuff -------------------
    def authenticate(self):
        self.conn.send(f'PASS {self.oauth_token}')
        self.conn.send(f'NICK {self.nick}')

        response = self.conn.receive()
        return (response and WELCOME_MSG in response)

    # CAPABILTIES 
    def init_capabilities(self):
        """ tw response:
        :tmi.twitch.tv CAP * ACK :twitch.tv/commands twitch.tv/tags
        """

        def cap_request_msg(cap):
            return f'CAP REQ :twitch.tv/{cap}'

        for cap in CAPS:
            msg = cap_request_msg(cap)
            self.conn.send(msg)
            

    def handle_cap_response(self, msg, *args, **kwargs):
        if 'ACK :' in msg:
            _, cap_data = msg.split('ACK')
            caps = cap_data.lstrip().split(' ') if ' ' in cap_data else [capdata] 
            caps = [c.split('/')[-1] for c in caps]
            for c in caps:
                _attr = f'cap_{c}'
                if hasattr(self, _attr):
                    setattr(self, _attr, True)
                else:
                    self.logger.warn(f'capability not known: {_attr}')

        elif 'NAK' in msg:
            _, cap = msg.split(':')
            self.logger.warn(f'capability {cap} denied!')

   # ----------------------- generic methods -------------------
    def send_message(self, message):
        self.conn.send(f'PRIVMSG {self.channel} :{message}')


    def join_channel(self, channel=None):
        if channel is None:
            channel = self.channel
        channel = channel if channel.startswith('#') else f'#{channel}'
        self.conn.send(f'JOIN {channel}')
    
    
    # ----------------------- Event Handlers -------------------
    def handle_ping(self, msg, *args, **kwargs):
        _, data = msg.split(" ")
        self.conn.pong(data)
        return


    def handle_join(self, *args, **kwargs):
        """ since twitch join/part behavior is inconsistent,
        just igore for now. Also we dont want to call out lurkers
        """
        pass


    def handle_part(self, *args, **kwargs):
        """ since twitch join/part behavior is inconsistent,
        just igore for now. Also we dont want to call out lurkers
        """
        pass



    def handle_roomstate(self, *args, **kwargs):
        pass


    def handle_userstate(self, *args, **kwargs):
        pass


    def handle_privmsg(self, msg, *args, **kwargs):
        flags = kwargs.pop('tags_enabled', False)
        if flags:
            msg = self._parse_msg_with_flags(msg)

        
        user_data, cmd, chan, data = msg.split(" ",3)
        
        user_name = self._parse_user_name(user_data)
        user_msg = data[1:]


        for func in self._triggers:
            func(user_name)
        
        self.logger.info(f'{self.timestamp} {user_name}: {user_msg}')
        if user_msg.startswith('!'):
            self.handle_command(user_name, user_msg)


    # ----------------------- Command Related Stuff -------------------
    def add_trigger(self, trigger):
        self._triggers.append(trigger)


    def register_command(self, plugin, command):
        try:
            if command in self._commands.keys():
                raise CommandAlreadyRegisterd(plugin.name, command)
            else:
                self._commands[command] = plugin

        except CommandAlreadyRegisterd as e:
            self.errors.add(e)


    def handle_command(self, user_name, command):
        """ parse commands that are prefixed and if command is known,
            call the matching handler
        """
        _cmd = command.rstrip()[1:]

        plugin = self._commands.get(_cmd, False)
        if plugin:
            return plugin.execute_command(_cmd, user_name=user_name)


        if _cmd in self.get_command_names():
            self.execute_command(_cmd, user_name)


    def _get_commands(self):
        cmds = set()
        for plugin in self.plugins.values():
            p_cmds = plugin.get_command_names()
            cmds = cmds.union(p_cmds)
        
        return cmds


    def commands(self, *args):
        """ get all available commands  and return a response method """
        cmds = self._get_commands()
        cmds_parsed = ' '.join([f'!{c}' for c in cmds])
        m = f'Commands are: {cmds_parsed}'
        self.send_message(m)


    def get_command_names(self):
        return set(['commands'])


    def execute_command(self, cmd_name, *args):
        """ this basically handles !commands """
        fnc = getattr(self, cmd_name, False)
        if fnc:
            return fnc(*args)


    # ----------------------- Message Handlers -------------------
    # parse messages recieved from twitch
    def get_msg_handler(self, msg):
        handlers = {
            TwitchMessageType.PRIVMSG: self.handle_privmsg,
            TwitchMessageType.PING: self.handle_ping,
            TwitchMessageType.CAP: self.handle_cap_response,
            TwitchMessageType.JOIN: self.handle_join,
            TwitchMessageType.PART:self.handle_part,
            TwitchMessageType.ROOMSTATE: self.handle_roomstate,
            TwitchMessageType.USERSTATE: self.handle_userstate
        }

        handler = next(iter(h for n, h in handlers.items() if n.contains(msg)), False)
        if not handler:
            self.logger.error(f'couldnt find handler for message\n####\n{msg}\n####')
        return handler


    def handle_msg(self, msg: str) -> None:
        """ main message parsing/handling method
            if we get a ping, return a pong
            else: parse the message/messages
        """
        
        if MULTILINE_MARKER in msg:
            # handle multi message
            msgs = msg.splitlines()
            for m in msgs:
                self._handle_msg(m)

        else:
            self._handle_msg(msg)

 

    def _handle_msg(self, msg: str) -> None:
        # check type of message
        msg = msg.rstrip()
        handler = self.get_msg_handler(msg)
        # check if caps
        tags_enabled = self.cap_tags
        if handler:
            return handler(msg, tags_enabled=tags_enabled)

        return False


    # ----------------------- Parsing Methods -------------------
    def _parse_user_name(self, part):
        part = part.lstrip()
        if part.startswith(':'):
            part = part[1:-1]
        try:
            marker = part.index("!")
            _user = part[:marker]
            return _user
        except ValueError as e:
            self.logger.error(e)
            self.logger.error(part)



    def _parse_msg_with_flags(self, msg):
        """ flagged messages look like this:
            @badge-info=;
            badges=broadcaster/1;
            client-nonce=459e3142897c7a22b7d275178f2259e0;color=#0000FF;
            display-name=lovingt3s;emote-only=1;
            emotes=62835:0-10;
            first-msg=0;
            flags=;
            id=885196de-cb67-427a-baa8-82f9b0fcd05f;
            mod=0;
            room-id=713936733;
            subscriber=0;
            tmi-sent-ts=1643904084794;turbo=0;user-id=713936733;
            user-type= :lovingt3s!lovingt3s@lovingt3s.tmi.twitch.tv PRIVMSG #lovingt3s :bleedPurple
        """

        part_tuples = msg.split(';')
        def split_tuple(t, marker='='):
            p = t.split(marker, 1)
            return p

        # todo: make this nice again
        part_tuples2 = [split_tuple(tp) for tp in part_tuples]
        try:
            parts = {p[0] : p[1] for p in part_tuples2}
        except IndexError as e:
            self.logger.error(e)
            self.logger.error(msg)

        msg_part = parts.get('user-type', False)
        if not msg_part:
            self.logger.error(f'not able to parse msg! \n{parts}')
            return
        
        _msg = msg_part.split(':', 1)[-1]

        return _msg


        
