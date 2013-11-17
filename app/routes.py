from ferris.core import routing, plugins
from app.controllers import Sessions

routing.add(Route('/login', Sessions, 'login', handler_method='login', methods=['GET', 'POST']))
routing.add(Route('/logout', Sessions, 'logout', handler_method='logout', methods=['GET', 'POST']))

# Routes all App handlers
routing.auto_route()

# Default root route
routing.default_root()


# Plugins
plugins.enable('settings')
plugins.enable('oauth_manager')
plugins.enable('template_tester')
