from google.appengine.ext import ndb
from ferris.core.ndb import util, BasicModel
from webapp2_extras.auth import InvalidAuthIdError, InvalidPasswordError
from webapp2_extras.appengine.auth.models import Unique, UserToken
from app.models.school import School
from extras.password_util import make_password, check_password
import logging
import time
import csv


# Heavily lifted from webapp2_extras.appengine.auth.models.User
# Parent = School
class Student(BasicModel):
    # The model used to reserve auth ids.
    unique_model = Unique
    # The model used to store tokens.
    token_model = UserToken
    
    sis_id = ndb.StringProperty()
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    grade_level = ndb.IntegerProperty()
    email = ndb.StringProperty()
    crypted_password = ndb.StringProperty()
    
    def get_id(self):
        return util.encode_key(self._key)
            
    def set_password(self, raw_password):
        """Sets the password for the current user

        :param raw_password:
          The raw password which will be hashed and stored
        """
        self.crypted_password = make_password(raw_password)

    @classmethod
    def get_by_auth_id(cls, auth_id):
        """Returns a user object based on a auth_id.

        :param auth_id:
          String representing a unique id for the user. Examples:

          - own:username
          - google:username
        :returns:
          A user object.
        """
        return cls.query(cls.email == auth_id).get()

    @classmethod
    def get_by_auth_token(cls, user_id, token):
        """Returns a user object based on a user ID and token.

        :param user_id:
          The user_id of the requesting user.
        :param token:
          The token string to be verified.
        :returns:
          A tuple ``(User, timestamp)``, with a user object and
          the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, 'auth', token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
          timestamp = int(time.mktime(valid_token.created.timetuple()))
          return user, timestamp

        return None, None

    @classmethod
    def get_by_auth_password(cls, auth_id, password):
        """Returns a user object, validating password.

        :param auth_id:
          Authentication id.
        :param password:
          Password to be checked.
        :returns:
          A user object, if found and password matches.
        :raises:
          ``auth.InvalidAuthIdError`` or ``auth.InvalidPasswordError``.
        """
        user = cls.get_by_auth_id(auth_id)
        if not user:
          raise InvalidAuthIdError()

        if not check_password(password, user.crypted_password):
          raise InvalidPasswordError()

        return user

    @classmethod
    def validate_token(cls, user_id, subject, token):
        """Checks for existence of a token, given user_id, subject and token.

        :param user_id:
          User unique ID.
        :param subject:
          The subject of the key. Examples:

          - 'auth'
          - 'signup'
        :param token:
          The token string to be validated.
        :returns:
          A :class:`UserToken` or None if the token does not exist.
        """
        return cls.token_model.get(user=user_id, subject=subject,
                                 token=token) is not None

    @classmethod
    def create_auth_token(cls, user_id):
        """Creates a new authorization token for a given user ID.

        :param user_id:
          User unique ID.
        :returns:
          A string with the authorization token.
        """
        return cls.token_model.create(user_id, 'auth').token

    @classmethod
    def validate_auth_token(cls, user_id, token):
        return cls.validate_token(user_id, 'auth', token)

    @classmethod
    def delete_auth_token(cls, user_id, token):
        """Deletes a given authorization token.

        :param user_id:
          User unique ID.
        :param token:
          A string with the authorization token.
        """
        cls.token_model.get_key(user_id, 'auth', token).delete()


    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
          The user_id of the requesting user.
        :param token:
          The token string to be verified.
        :returns:
          A tuple ``(User, timestamp)``, with a user object and
          the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])
        if valid_token and user:
          timestamp = int(time.mktime(valid_token.created.timetuple()))
          return user, timestamp

        return None, None
     
    @classmethod
    def import_csv(cls, reader):
        for row in csv.DictReader(reader):
            school_key = School.key_for_sis_id(row['school_id'])
            student = cls.find_by_sis_id(row['sis_id'])
            crypted_password = make_password(row['password'])
            if student is None:
                student = cls(
                    parent=school_key,
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    sis_id=row['sis_id'],
                    grade_level=int(row['grade_level']),
                    email=row['email'],
                    crypted_password=crypted_password
                )
                student.put()
                logging.info("inserted student: %s" % row)
            else:
                # cannot change student from one school to another?
                student.first_name = row['first_name']
                student.last_name = row['last_name']
                student.sis_id = row['sis_id']
                student.grade_level = int(row['grade_level'])
                student.email = row['email']
                student.crypted_password = crypted_password
                student.put()
                logging.info("updated student: %s" % row)
