# Import Third-Party
from bottle import Bottle, Route
from bottle import static_file

# Import Home-Grown
from src.utils.logger import get_logger
logger = get_logger('Server')

class Server(Bottle):
    """ Wrapper around Bottle to enable adding routes programmaticly"""

    def __init__(self, app, *args, **kwargs):
        self.app = app
        super().__init__()
        
        static_files = kwargs.get('static_files', False)
        if static_files:
            self.init_static_files(static_files)



    def init_static_files(self, static_files):
        self.static_files = static_files
        self.add_route('/static/<filename>', 'GET', self.get_app_static)
    

    def get_app_static(self, filename):
        return static_file(filename, root=self.static_files)


    def get_app_url(self, endpoint, *args):
        endpoint = endpoint + '/' if not endpoint.endswith('/') else endpoint
        combined_url = endpoint + '/'.join([a for a in args])
        return super().get_url(combined_url)


    def add_route(self, rule, http_method, callback):
        route = Route(self, rule, http_method, callback)
        super().add_route(route)

