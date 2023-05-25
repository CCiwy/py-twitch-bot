from src.plugins.base import PluginWithEndpoint
from bottle import request, redirect


GITHUB_LINK = 'http://www.github.com/CCiwy'
#GITHUB_CURRENT = ''
GITHUB_CURRENT = 'https://github.com/CCiwy/py-twitch-bot'
NEOVIM_CFG = 'https://github.com/CCiwy/nvim_config'
NO_PROJECT_SET = 'Quesnok did not link a current project. Please remind him to push to github!'

class GithubPlugin(PluginWithEndpoint):
    endpoint = '/github'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        

    def start(self):
        pass

    def _make_routes(self):
        route_data = [
                ("GET", "/all", self.current),        
                ("POST", "/update", self.update) 
                ]
        
        for entry in route_data:
            self.make_route(*entry)


    def update(self):
        _updates = self.request.forms
        self.update_commands(_updates)
        return redirect('/github/all')
    # todo: reimplement


    def current(self):
        _responses = {cmd._command : cmd.get_data() for cmd in self._commands.values()}
        return self.template('github', handlers=_responses)


    def current_project(self):
        if not len(GITHUB_CURRENT):
            return NO_PROJECT_SET
        return GITHUB_CURRENT





