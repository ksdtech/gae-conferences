# process a 403 for our application
# if request was to /students, set up login_url to /login
# otherwise set up login_url to appengine Users service

import db_auth
from google.appengine.api import users
from ferris.core.template import render_template
import json
import logging

def handle_403(request, response, exception):
    logging.exception(exception)
    response.set_status(403)

    if 'application/json' in request.headers.get('Accept') or request.headers.get('Content-Type') == 'application/json':
        response.text = unicode(json.dumps({
            'error': str(exception), 
            'code': 403
        }, encoding='utf-8', ensure_ascii=False))

    else:
        template = ('errors/403.html', 'errors/500.html')
        login_url = None
        if request.path.startswith('/students'):
            login_url = db_auth.create_login_url(request.url)
            login_name = 'Student log in'
        else:
            login_url = users.create_login_url(request.url)
            login_name = 'Teacher log in'
        context = { 'request': request, 'exception': exception, 'login_url': login_url, 'login_name': login_name }
        response.content_type = 'text/html'
        response.text = render_template(template, context)
