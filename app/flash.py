from ferris.core.handler import Handler

class FlashHandler(Handler):
    def is_json_request(self):
        return (('json' in self.components and self.components.json.render_as_json)
            or self.request.content_type == 'application/json')
    
    def flash(self, message, type='info'):
        """
        Adds the given message to the list of "flash" messages to show to the user on the next page.
        This never occurs for json requests.
        """
        if self.is_json_request():
            return

        flash = self.session.get('__flash', list())
        flash.append((message, type))
        self.session['__flash'] = flash
