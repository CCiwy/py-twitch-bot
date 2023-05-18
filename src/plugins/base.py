from bottle import jinja2_template as template
from bottle import redirect
from bottle import request


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


    def add_command(self, ident: str, *args, **kwargs) -> None:
        cmd_cls = StaticCommand

        if kwargs.get('callback', False):
            cmd_cls = CallbackCommand

        # initialize command
        cmd = cmd_cls(self, ident, *args, **kwargs)
        self._commands[ident] = cmd
        
    

    def get_save(self):
        return {attr_name : getattr(self, attr_name, False) for attr_name in self._save_attrs}
    def register_command(self, command: str):
        self.handler.register_command(self, command)




    def get_command(self, ident):
        """ this is called from within our application """
        return self._commands.get(ident, False)

    
    def get_command_names(self) -> set[str]:
        _commands = set([c.command for c in self._commands.values() if c.is_active])
        return _commands
   

    def execute_command(self, cmd_name, *args, **kwargs):
        # todo: cmd_name does not equal ident
        command = self._commands[cmd_name]
        message = command.execute(*args, **kwargs)
        

        if message:
            self.handler.send_message(message)

    def load(self, save_game):
        for attr, value in save_game.items():
            if attr in self._save_attrs:
                setattr(self, attr, value)

    def update_commands(self, _updates):
        for ident, new_data in _updates.items():
            if ident in self._commands:
                self._update_command(ident, new_data)


    def _update_command(self, ident, new_data):
        command = self.get_command(ident)
        if new_data != command.get_data():
            # todo: ident does not equal command
            command.set_data(new_data)


        



class PluginWithEndpoint(BotPlugin):
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
