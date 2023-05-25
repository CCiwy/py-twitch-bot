from src.plugins.base import PluginWithEndpoint



class MessagesPlugin(PluginWithEndpoint):
    """ wrapper around simple responses """
    endpoint = '/messages'

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)       

    def start(self):
       pass 


    def _make_routes(self):
        self.make_route("GET", "/all", self.list_responses, sidebar_element=True)
        self.make_route("POST", "/update", self.update)
        self.make_route("GET", "/activate/<command_ident>", self.toggle_command_active)
        self.make_route("GET", "/new", self.new_command, sidebar_element=True)


    def toggle_command_active(self, command_ident):
        command = self.get_command(command_ident, internal=True)
        if command:
            command.toggle_active()
        return self.redirect('/messages/all')


    def list_responses(self):
        return self.template('messages',handlers=self._commands)



    def update(self):
        self.update_commands(self.request.forms)
        return self.redirect('/messages/all')







