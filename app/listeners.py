"""
Central place to store event listeners for your application,
automatically imported at run time.
"""
import logging
from ferris.core import events, settings

def require_auth_domain(controller):
    user = controller.user
    if user:
        domain = user.email().split('@').pop()
        allowed_domains = settings.get('app_config')['allowed_auth_domains']
        if domain not in allowed_domains:
            message = "Your domain, %s, does not have access to this application" % domain
            return False, message

    return True

@events.on('controller_before_authorization')
def inject_authorization_chains(controller, authorizations):
    authorizations.insert(0, require_auth_domain)
