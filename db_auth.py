from ferris.core.auth import predicate_chain, prefix_predicate, action_predicate, route_predicate

def require_db_user(controller):
    """
    Requires that a user is logged in
    """
    if not controller.db_user:
        return (False, "You must be logged in")
    return True
