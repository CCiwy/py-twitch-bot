class BaseCommand(object):
    """ wrapper around chatbot responses to commands """

    def __init__(self, plugin, ident: str, *args, **kwargs) -> None:
        self.plugin = plugin
        
        self._ident = ident
        self._command = False
        self._data = False
        self._is_active = False

        command = kwargs.get('command')
        if command:
            self.set_command(command)


        data = kwargs.get('data')
        if data:
            self.set_data(data)

        # ACTIVE 
        active = True
        #active = kwargs.get('')
        if active:
            self.toggle_active()


    @property
    def command(self):
        return self._command


    @property
    def ident(self):
        return self._ident
   

    def is_active(self):
        return self._is_active


    def get_data(self):
        """ if message is active return data else False """
        return self._data


    def is_command(self, cmd):
        return cmd == self._command


    def toggle_active(self):
        print(f'toggle {self.ident} {self._is_active}')
        self._is_active = not self._is_active


    def set_command(self, command):
        self._command = command
        self.plugin.register_command(self._command)


    def set_data(self, data):
        self._data = data


    def get_save(self):
        """ get the current state
            in a way our application can store it to file/database
            possible options: string/dict
        """
        
        return {self.ident : self.get_data()}



class StaticCommand(BaseCommand):

    def execute(self, *args, **kwargs):
        if self.is_active:
            return self.get_data()
        return False


class CallbackCommand(BaseCommand):
    def __init__(self, plugin, ident, *args, **kwargs):
        self.callback = False
        callback = kwargs.get('callback', False)

        super().__init__(plugin, ident, *args, **kwargs)
        if callback:
            self.bind(callback)


    def bind(self, callback):
        if isinstance(callback, str):
            callback = getattr(self.plugin, callback, False)
        self.callback = callback



    def execute(self, *args, **kwargs):
        if self.is_active and self.callback:
            return self.callback(self, *args, **kwargs)
        return False
