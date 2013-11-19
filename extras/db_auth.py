from google.appengine.api import users
from webapp2_extras.auth import get_auth
from ferris.core.auth import predicate_chain, prefix_predicate, action_predicate, route_predicate
import urllib

def add_db_user_meta(controller):
    controller.db_user = None
    db_user = get_auth().get_user_by_session()
    if db_user and db_user['user_id']:
        auth_key = controller.util.decode_key(db_user['user_id'])
        controller.db_user = auth_key.get()


def create_login_url(dest_url=None):
    return "/login?next=%s" % urllib.quote(dest_url, safe='/')

    
def require_db_user(controller):
    """
    Requires that a user is logged in
    """
    if not controller.db_user:
        return (False, "You must be logged in")
    return True

require_db_user_for_action = predicate_chain(action_predicate, require_db_user)
