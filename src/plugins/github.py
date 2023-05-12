from src.plugins.base import PluginWithEndpoint


GITHUB_LINK = 'http://www.github.com/CCiwy'
#GITHUB_CURRENT = ''
GITHUB_CURRENT = 'https://github.com/CCiwy/py-twitch-bot'
NEOVIM_CFG = 'https://github.com/CCiwy/nvim_config'
NO_PROJECT_SET = 'Quesnok did not link a current project. Please remind him to push to github!'

class GithubPlugin(PluginWithEndpoint):
    endpoint = '/github'


    def __init__(self, *args, **kwargs):
        self._responses = {}

        super().__init__(*args, **kwargs)
        
        self._save_attrs  = ['_responses']


    def start(self):
        self._init_responses()


    def make_routes(self):
        routes = [
                ("GET", "/index", self.index),        
                ("GET", "/current",self.current),        
                
                ]

        return self.endpoint, routes
    

    def index(self):
        return 'INDEX!!!!'


    def current(self):
        return self._responses


    def _init_responses(self):
        _responses = {
            'github' : GITHUB_LINK,
            'neovim' : NEOVIM_CFG
        }

        for cmd, msg in _responses.items():
            if not self._responses.get(cmd,False):
                self._responses[cmd] = msg


    def current_project(self):
        if not len(GITHUB_CURRENT):
            return NO_PROJECT_SET
        return GITHUB_CURRENT


    def get_command_names(self) -> set[str]:
        return set(self._responses.keys())

    
    def execute_command(self, cmd_name, *args):
        response = self._responses[cmd_name]
        self.handler.send_message(response)


    def get(self, msg, *args):
        return self._responses.get(msg, False)


