# Import Built-Ins
import json
import os

from datetime import date
from datetime import datetime as dt
from threading import Thread

# Import Third-Party
from bottle import run as bottle_run


# Import Home-Grown
from src.chat import Chat
from src.server import Server

from src.plugins import PLUGINS

from src.utils.logger import get_logger
from src.utils.configparser import Config

class ErrorLog:
    def __init__(self) -> None:
        self._entries = []

    @property
    def timestamp(self):
        return str(dt.now())

    def add(self, msg):
        line = f'{self.timestamp}: {msg}'
        self._entries.append(line)


    def get(self):
        return self._entries

    def get_string(self):
        return '<br>'.join([e for e in self._entries])


class App:
    running = False


    def __init__(self, *args):
        self.logger = get_logger('APP')
        self.errors = ErrorLog()
        self.config = Config('..')
        self.config.from_pyfile('config.py')
        self.chat = Chat(self, *args)
        self.server = Server(self, static_files=self.config.STATIC_FILE_DIR)


        self._plugins = {}


    
    def _start(self):
        self._init_server()
        self._init_chat()
        self._init_plugins()
        self._init_error_handling()
        self.load()


    def _init_server(self):
        self.server_thread = Thread(target=self.run_server, name='server')
        self.server_thread.daemon = True
        self.server_thread.start()
        

    def _init_chat(self):
        self.chat.start()
        self.chat_thread = Thread(target=self.chat.run, name='chat')
        self.chat_thread.daemon = True
        self.chat_thread.start()


    def _load_config(self, file_path):
        with open(file_path, 'r') as f:
            content = json.load(f)
            return content
    

    def _init_plugins(self):
        config_path = self.config.CONFIG_DIR + 'default.json'
        config = self._load_config(config_path) 
        for plugin_cls in PLUGINS:
            plugin = plugin_cls(self)
            self.__init_plugin(plugin, config)

    def _init_error_handling(self):
        route = ("/errors/" , "GET", self.errors.get_string)
        self.server.add_route(*route)


    @property
    def plugins(self):
        return self._plugins

    # ----------------------- Plugin related -------------------

    def __init_plugin(self, plugin, config):
        config = config.get('plugins') #todo: make this clean
        plugin_config = config.get(plugin.name, False)
        #self.logger.debug(f'got conf for {plugin.name} {bool(plugin_config)}') 
        if plugin_config:
            plugin.load_config(plugin_config)
        
        # init potential trigger methods
        if hasattr(plugin, 'trigger'):
            self.chat.add_trigger(plugin.trigger)


        # init potential plugin http-endpoints
        if hasattr(plugin, 'endpoint'):
            self._make_plugin_routes(plugin)

        
        # add plugin
        self.logger.debug(f'adding plugin: {plugin.name}')
        self._plugins[plugin.name] = plugin
            
        plugin.start()


    def _make_plugin_routes(self, plugin):    
        #self.logger.debug(f'Initing routes for {plugin.name}')
        path_base, routes = plugin.make_routes()
       
        for http_method, rel_path, callback in routes:
            abs_path = f'{path_base}{rel_path}'
            #self.logger.debug(f'init Route: {abs_path} -> {callback}')
            self.server.add_route(abs_path, http_method, callback)





    ## ----------------------- Plugin saved data related -------------------
    def load(self):
        # load config file "savegame"
        save_game = self._load_savegame()
        if not save_game:
            return

        for plugin_name, plugin_save in save_game.items():
            p = self._plugins.get(plugin_name, False)
            if not p:
                self.logger.error(f'could not find plugin {p}.')
                continue

            p.load_state(plugin_save)
    

    def __savegame_file_name(self):
        _today = str(date.today())
        file_name = f'save_{_today}.json'
        return file_name

    
    def _load_savegame(self):
        file_name = self.__savegame_file_name()
        if os.path.isfile(file_name):
            self.logger.info('found savegame for today')
            with open(file_name, 'r') as fp:
                save_game = json.load(fp)
                return save_game

        return False


    def save(self):
        save_game = {}
        for plugin in self._plugins.values():
            save_game[plugin.name] = plugin.get_save()
        

        file_name = self.__savegame_file_name()
        with open(file_name, 'w') as fp:
            json.dump(save_game, fp)

        self.logger.info(f'saved to file {file_name}')



    def start(self):
        self._start()
        self.is_running = True
        self.logger.info(f'APPLICATION STARTUP')
        

    def run_server(self):
        bottle_run(self.server, host='localhost', port=8888)


    def run(self):
        pass


    def exit(self):
        self.logger.info('App shutting down')
        self.save()
        self.chat.exit()
        self.chat_thread.join()
        self.server_thread.join()
        
        self.is_running = False
        self.logger.info('Shutdown')

