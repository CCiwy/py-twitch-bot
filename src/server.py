# Import Third-Party
from bottle import Bottle, Route

from src.utils.logger import get_logger

logger = get_logger('Server')

class Server(Bottle):
    """ Wrapper around Bottle to enable adding routes programmaticly"""

    def __init__(self, app):
        self.application_context = app
        super().__init__()

    def get_app_url(self, endpoint, *args):
        endpoint = endpoint + '/' if not endpoint.endswith('/') else endpoint
        combined_url = endpoint + '/'.join([a for a in args])
        self.application_context.logger.debug(f'combined_url: {combined_url} <= {args}')
        return super().get_url(combined_url)

    def add_route(self, rule, http_method, callback):
        route = Route(self, rule, http_method, callback)
        super().add_route(route)

