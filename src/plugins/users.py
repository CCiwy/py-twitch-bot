from src.plugins.base import PluginWithEndpoint

class UsersPlugin(PluginWithEndpoint):
    template_path = 'users'
    endpoint = '/users'


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)



    def start(self):
        self.add_command('first', command='first', data='', callback=self.first)
        self.add_command('lurk', command='lurk', callback=self.lurk)



    def _make_routes(self):
        self._routes = [
            ("GET", "/lurkers", self.list_lurkers),
            ("GET", "/first", self.response_first),
        ]


    def response_first(self):
        _first = self._commands.get('first').get_data()
        return self.template(self.template_path, first=_first)


    def list_lurkers(self):
        _lurkers = self._commands.get('lurkers').get_data()

        return self.template(self.template_path, lurkers=_lurkers)


        
    def trigger(self, user_name):
        cmd = self._commands.get('lurk')
        if not cmd:
            return

        lurk_data = cmd.get_data()
        if not lurk_data:
            return
        _lurkers = lurk_data.get('current')
        if user_name in _lurkers:         
            _lurkers.remove(user_name)
        
            msg = f'{user_name} is back from lurking. Welcome back!'
            self.handler.send_message(msg)     


    def first(self, command, *args, **kwargs):
        user_name = kwargs.get('user_name')
        data = command.get_data()
        if data:
            if data == user_name:
                msg = f'You already were the first, {user_name}!' 
            else:
                msg = f'Today {data} was the first'
        else:
            msg = f'Congratulations {user_name}, you were first!'
            command.set_data(user_name)

        return msg
        


    def lurk(self, command, *args, **kwargs):
        user_name = kwargs.get('user_name')
        data = command.get_data()
        if not data or not len(data):
            data = {
                    'today' : [],
                    'current' : []
            }

        
        _lurkers_today = data.get('today')
        _lurkers = data.get('current')

        if not user_name in _lurkers:
            _lurkers.append(user_name)
        
        if not user_name in _lurkers_today:
            _lurkers_today.append(user_name)
        
        command.set_data(data)
        msg = f'{user_name} is now lurking. Thanks for the lurk!'
        return msg


