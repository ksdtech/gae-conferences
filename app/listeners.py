"""
Central place to store event listeners for your application,
automatically imported at run time.
"""
import logging
import webapp2
from ferris.core.events import on
from settings import app_config

def set_log_level(level_name):
    lvl = { 
        'CRITICAL': logging.CRITICAL, 
        'ERROR': logging.ERROR, 
        'WARNING': logging.WARNING, 
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG }.get(level_name, None)
    if lvl:
        logging.error('setting log level to %s - %s' % (level_name, lvl))
        logging.getLogger().setLevel(lvl)
    else:
        logging.error('could not parse log level to %s' % level_name)

set_log_level(app_config['log_level'])


@on('handler_is_authorized')
def is_authorized(handler):
    pass


@on('before_template_render')
def before_template_render(name, *args, **kwargs):
    pass
