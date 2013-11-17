from passlib.apps import django_context

def check_password(password, encoded, setter=None, user_key=None):
    valid = False

    if password and not password.startswith("!"):
        if setter and user_key:
            valid, new_hash = django_context.verify_and_update(password, encoded)
            if valid and new_hash:
                setter(user_key, new_hash)
        else:
            valid = django_context.verify(password, encoded) 

    return valid

def make_password(password, salt=None):
    encoded = "!"
    if password:
        if salt:
            encoded = django_context.encrypt(password, salt=salt)
        else:
            encoded = django_context.encrypt(password, salt_size=12)
    return encoded
