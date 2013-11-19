import fix_imports

# Import the application
import settings
import ferris
import ferris.app
import ferris.deferred_app
import ferris.routes
import app.routes
import app.listeners
from app.exception_handlers import handle_403

from ferris.core import settings

main_app = ferris.app.app  # Main application
main_app.error_handlers[403] = handle_403

deferred_app = ferris.deferred_app.app  # Deferred application

appstats_settings = settings.get('appstats', {})

if (appstats_settings.get('enabled', False) and ferris.app.debug) or appstats_settings.get('enabled_live', True):
    from google.appengine.ext.appstats import recording
    main_app = recording.appstats_wsgi_middleware(main_app)
