from bottle import jinja2_template as template


class BotPlugin:
    """ plugin base class. might use as protocol """
    _save_attrs = []
    _name = False
    instances = {}


    def __init__(self, handler):
        self.handler = handler
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
    

    def base_routes(self):
        return [("GET", "/health", self.health)]
    def template(self, tpl_name, **kwargs):
        kwargs["navigation"] = self.navigation_links()
        return template(tpl_name, **kwargs)

    def health(self):
        ep = self.endpoint
        return self.template('health.tpl', ep=ep)
