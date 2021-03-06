from ferris.core.ndb import ndb
from protopigeon import Message, model_message, to_message, messages
import logging


def list_message(message_type):
    name = message_type.__name__ + 'List'
    fields = {
        'items': messages.MessageField(message_type, 1, repeated=True),
        'next_page': messages.StringField(2),
        'previous_page': messages.StringField(3),
        'limit': messages.IntegerField(4),
        'count': messages.IntegerField(5),
        'page': messages.IntegerField(6)
    }
    return type(name, (messages.Message,), fields)


class Messaging(object):
    def __init__(self, controller):
        self.controller = controller
        self.transform = False

        # Create a Message class if needed
        if not hasattr(self.controller.meta, 'Message'):
            if not hasattr(self.controller.meta, 'Model'):
                raise ValueError('Controller.Meta must have a Message or Model class.')
            setattr(self.controller.meta, 'Message', model_message(self.controller.meta.Model))

        # Prefixes to automatically treat as messenging views
        if not hasattr(self.controller.meta, 'messaging_prefixes'):
            setattr(self.controller.meta, 'messaging_prefixes', ('api',))

        # Variable names to check for data
        if not hasattr(self.controller.meta, 'messaging_variable_names'):
            setattr(self.controller.meta, 'messaging_variable_names', ('data',))

        if hasattr(self.controller, 'scaffold'):
            self.controller.meta.messaging_variable_names += (self.controller.scaffold.plural, self.controller.scaffold.singular)

        # Events
        self.controller.events.before_startup += self._on_before_startup
        self.controller.events.before_render += self._on_before_render

    def _on_before_startup(self, controller, *args, **kwargs):
        if controller.route.prefix in self.controller.meta.messaging_prefixes:
            self.activate()

    def activate(self):
        self.transform = True
        self.controller.meta.Parser = 'Message'
        self.controller.meta.change_view('Message')

        if hasattr(self.controller, 'scaffold'):
            self.controller.scaffold.flash_messages = False
            self.controller.scaffold.redirect = False

    __call__ = activate

    def _get_data(self):
        for v in self.controller.meta.messaging_variable_names:
            data = self.controller.context.get(v, None)
            if data:
                return data

    def _transform_data(self, data):
        if isinstance(data, Message):
            return data
        if isinstance(data, (list, ndb.Query)):
            return self._transform_query(data)
        if isinstance(data, ndb.Model):
            return self._transform_entity(data)
        return data

    def _transform_query(self, query):
        ListMessage = list_message(self.controller.meta.Message)
        items = [self._transform_entity(x) for x in query]
        next_page_link = None
        prev_page_link = None
        limit = None
        count = len(items)
        page = None

        if 'pagination' in self.controller.components:
            previous_cursor, current_cursor, next_cursor, page, limit, count = self.controller.components.pagination.get_pagination_info()

            if next_cursor:
                next_page_link = self.controller.uri(_pass_all=True, cursor=next_cursor, _full=True)

            if previous_cursor is not None:
                prev_page_link = self.controller.uri(_pass_all=True, cursor=previous_cursor, _full=True)


        return ListMessage(
            items=items,
            next_page=next_page_link,
            previous_page=prev_page_link,
            limit=limit,
            count=count,
            page=page)

    def _transform_entity(self, entity):
        if hasattr(self.controller.meta, 'messaging_transform_function'):
            return self.controller.meta.messaging_transform_function(entity, self.controller.meta.Message)
        return to_message(entity, self.controller.meta.Message)

    def _on_before_render(self, *args, **kwargs):
        if self.transform:
            self.controller.context['data'] = self._transform_data(self._get_data())
