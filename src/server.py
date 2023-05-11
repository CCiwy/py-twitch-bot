# Import Third-Party
from bottle import Bottle, Route



class Server(Bottle):
    """ Wrapper around Bottle to enable adding routes programmaticly"""

    def __init__(self, app):
        self.app = app
        super().__init__()
        self.init_plugins()



    def add_route(self, http_method, path, callback):
        route = Route(self, path, http_method, callback)
        super().add_route(route)

