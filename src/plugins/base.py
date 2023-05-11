class BotPlugin:
    """ plugin base class. might use as protocol """
    _save_attrs = []
    _name = False
    def __init__(self, handler):
        self.handler = handler


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
    endpoint = True


    def health(self):
        return f'Endpoint {self.name} is working!'
