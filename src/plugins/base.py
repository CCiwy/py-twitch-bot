from bottle import jinja2_template as template
from bottle import redirect
from bottle import request



# Import Home-grown

#from src.plugins.chat_commands import FallbackCommand
from src.plugins.chat_commands import StaticCommand
from src.plugins.chat_commands import CallbackCommand


class AppRoute:
    def __init__(self, rule, callback, http_method="GET", sidebar_element=False, param=False):
        self.rule = rule
        self.callback = callback
        self.http_method = http_method
        self.param = self._set_param(param)

        self.is_sidebar_element = (sidebar_element and not http_method == "POST")


    def get(self):
        """ return the route data as called in endpoint.make_routes """
        rule = self.rule if not self.param else f'{self.rule}/{self.param}'
         
        return (self.http_method, rule, self.callback)
 

    def _set_param(self, param):
        if param and param.startswith('<') and param.endswith('>'):
            return param 
        
        return False


class BotPlugin:
    """ plugin base class. might use as protocol """
    _name = False
    instances = {}


    def __init__(self, app):
        self.app = app
        self.handler = app.chat
        self.instances[self.name] = self
        self._commands = {}


    @property
    def name(self):
        if not self._name:
            cls_name = self.__class__.__name__
            _name = cls_name.lower().replace('plugin', '')
            self._name = _name
        return self._name       


    def load_config(self, config):
        commands = config.get('data', False)
        if commands:
            for cmd, data in commands.items():
                self.add_command(cmd, command=cmd, data=data)


    def add_command(self, ident: str, *args, **kwargs) -> None:
        cmd_cls = StaticCommand

        if kwargs.get('callback', False):
            cmd_cls = CallbackCommand

        # initialize command
        cmd = cmd_cls(self, ident, *args, **kwargs)
        self._commands[ident] = cmd
        
    

    def register_command(self, command: str):
        self.handler.register_command(self, command)




    def get_command(self, ident, internal=False):
        """ this is called from within our application """
        command = self._commands.get(ident, False)
        if command and  (internal or command.is_active):
            return command

        return False
    
    def get_command_names(self) -> set[str]:
        _commands = set([c.command for c in self._commands.values() if c.is_active])
        return _commands
   

    def execute_command(self, cmd_name, *args, **kwargs):
        # todo: cmd_name does not equal ident
        command = self.get_command(cmd_name)
        if not command:
            return
        message = command.execute(*args, **kwargs)
        

        if message:
            self.handler.send_message(message)


    def update_commands(self, _updates):
        for ident, new_data in _updates.items():
            if new_data and ident in self._commands:
                self._update_command(ident, new_data)


    def _update_command(self, ident, new_data):
        command = self.get_command(ident)
        if new_data != command.get_data():
            # todo: ident does not equal command
            command.set_data(new_data)


    def get_save(self):
        return {ident : cmd.get_data() for ident, cmd in self._commands.items()}
        



    def load_state(self, save_game):
        """ load current data after restart from json file savegame for current date """
        _save_game = save_game.get('_responses', False)
        save_game = _save_game if _save_game else save_game

        for ident, data in save_game.items():
            # value should be a small config
            command = self.get_command(ident)
            command.set_data(data)
        


class Endpoint:
    endpoint = False
    request = request
    _routes = False 
    

    def base_routes(self):
        return [
            ("GET", "/index", self.index),
            ("GET", "/health", self.health),
        ]


    def make_routes(self):
        if not self._routes:
            self._make_routes()
        return self.endpoint, self._routes


    def get_endpoint_routes(self):
        """ method, rule, callback"""
        rules = [r for (m, r, _) in self._routes if m in 'GET']
        return [r[1:] if r.startswith('/') else r for r in rules]



    @property
    def template_context(self):
        context = {}
        context["navigation"] = self._navigation_links()
        context["get_url"] = self.app.server.get_app_url
        context["rules"] = self.get_endpoint_routes()
        context["endpoint"] = self.endpoint
        return context


    def _navigation_links(self):
        return {p_name: p.endpoint for p_name, p in BotPlugin.instances.items() if hasattr(p, 'endpoint')}


    def template(self, tpl_name, **kwargs):
        kwargs["template_context"] = self.template_context
        return template(tpl_name, **kwargs)


    def redirect(self, route):
        return redirect(route)


    def index(self):
        return self.template('index.tpl', endpoint=self.endpoint)


    def health(self):
        ep = self.endpoint
        return self.template('health.tpl', ep=ep)



class PluginWithEndpoint(BotPlugin, Endpoint):
    pass
