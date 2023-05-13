from bottle import jinja2_template as template
from bottle import redirect
from bottle import request


class BotPlugin:
    """ plugin base class. might use as protocol """
    _save_attrs = []
    _name = False
    instances = {}


    def __init__(self, app):
        self.app = app
        self.handler = app.chat
        self.instances[self.name] = self

    @property
    def name(self):
        if not self._name:
            cls_name = self.__class__.__name__
            _name = cls_name.lower().replace('plugin', '')
            self._name = _name
        return self._name       
        

    def get_save(self):
        return {attr_name : getattr(self, attr_name, False) for attr_name in self._save_attrs}
        


    def load(self, save_game):
        for attr, value in save_game.items():
            if attr in self._save_attrs:
                setattr(self, attr, value)
        



class PluginWithEndpoint(BotPlugin):
    endpoint = False
    request = request


    def base_routes(self):
        return [
            ("GET", "/index", self.index),
            ("GET", "/health", self.health),
                ]



    @property
    def template_context(self):
        context = {}
        context["navigation"] = self._navigation_links()
        context["get_url"] = self.app.server.get_app_url
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
