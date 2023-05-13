from src.plugins.base import PluginWithEndpoint


# DEFINE DEFAULT ENTRIES

#TODAY = 'Today we are working on Twitch Bot. theoal is to have some !commands and also some moderation capabilities aswell as some stats'
TODAY = 'Today we will combine bottle.py with our our twitch bot to control it via browser'
WADDUP = 'Currently refactoring code and killing bugs'

MUTED = '@Quesnok you are muted' # todo: check how advanced messages work
GITHUB_LINK = 'http://www.github.com/CCiwy'
GITHUB_CURRENT = ''
#GITHUB_CURRENT = 'https://github.com/CCiwy/py-starlette-base'
NEOVIM_CFG = 'https://github.com/CCiwy/nvim_config'

class MessagesPlugin(PluginWithEndpoint):
    """ wrapper around simple responses """
    endpoint = '/messages'

    def __init__(self, *args, **kwargs):
        self._responses = {}

        super().__init__(*args, **kwargs)
        
        self._save_attrs  = ['_responses']


    def start(self):
        self._init_responses()


    def _make_routes(self):
        self._routes = [
            ("GET", "/all", self.list_responses),
            ("POST", "/update", self.update_response),
        ]



    def list_responses(self):
        return self.template('messages',handlers=self._responses)


    def _init_responses(self):
        _responses = {
            'waddup' : WADDUP,
            'muted' : MUTED,
            'today' : TODAY
            
        }

        for cmd, msg in _responses.items():
            if not self._responses.get(cmd,False):
                self._responses[cmd] = msg

    def get_command_names(self) -> set[str]:
        return set(self._responses.keys())

    
    def execute_command(self, cmd_name, *args):
        response = self._responses[cmd_name]
        self.handler.send_message(response)


    def get(self, msg, *args):
        return self._responses.get(msg, False)



