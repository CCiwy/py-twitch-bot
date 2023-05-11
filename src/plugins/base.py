class BotPlugin:
    """ plugin base class. might use as protocol """
    _save_attrs = []
        
    def __init__(self, handler):
        self.handler = handler


    @property
    def name(self):
        return self.__class__.__name__.lower()
       
        
    def index(self):
        return f'Endpoint {self.name} WORKS!'


    def get_save(self):
        return {attr_name : getattr(self, attr_name, False) for attr_name in self._save_attrs}
        


    def load(self, save_game):
        for attr, value in save_game.items():
            if attr in self._save_attrs:
                setattr(self, attr, value)
        


