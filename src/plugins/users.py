from src.plugins.base import PluginWithEndpoint
from bottle import template

class UsersPlugin(PluginWithEndpoint):
    template_path = 'src/users.tmpl'
    endpoint = '/users'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._save_attrs = ['_lurkers_today', '_lurkers', '_first_chatter']

        self._lurkers_today = []
        self._lurkers = []

        self._first_chatter = False

    def start(self):
        pass

    def get_command_names(self) -> set[str]:
        commands = set(['first','lurk'])
        return commands



    def make_routes(self):
        routes = [
            ("GET", "/health", self.health),
            ("GET", "/lurkers", self.list_lurkers)
        ]
        return self.endpoint, routes


    def list_lurkers(self):
        return template(self.template_path, lurkers=self._lurkers)


    def execute_command(self, cmd_name: str, *args):
        fnc = getattr(self, cmd_name, False)
        if fnc:
            fnc(*args)

        
    def trigger(self, user_name):
        if user_name in self._lurkers:         
            self._lurkers.remove(user_name)
            msg = f'{user_name} is back from lurking. Welcome back!'
            self.handler.send_message(msg)     


    def first(self, user_name):
        if self._first_chatter:
            if user_name == self._first_chatter:
                msg = f'You already were the first, {user_name}!' 
            else:
                msg = f'Today {self._first_chatter} was the first'
        else:

            msg = f'Congratulations {user_name}, you were first!'
            self._first_chatter = user_name


        self.handler.send_message(msg)

            

    def lurk(self, user_name):
        if user_name not in self._lurkers_today:
            self._lurkers_today.append(user_name)

        if user_name not in self._lurkers:
            self._lurkers.append(user_name)
            msg = f'{user_name} is now lurking. Thanks for the lurk!'
            self.handler.send_message(msg)


