import hmac
import time
import json
import base64
import hashlib

from core import settings

from social.utils import parse_qs, constant_time_compare, handle_http_errors
from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthException, AuthCanceled, AuthUnknownError, \
                              AuthMissingParameter


class SITCONOAuth2(BaseOAuth2):
    """SITCON OAuth2 authentication backend"""
    name = 'sitcon'
    RESPONSE_TYPE = 'code'
    ID_KEY = 'username'
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = settings.SITCON_OAUTH2_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.SITCON_OAUTH2_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = settings.SITCON_OAUTH2_REVOKE_TOKEN_URL
    REVOKE_TOKEN_METHOD = 'DELETE'
    USER_DATA_URL = settings.SITCON_OAUTH2_USER_DATA_URL
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('access_type', 'access_type', True),
    ]

    def user_data(self, access_token, *args, **kwargs):
        params = {
                'access_token': access_token,
                }
        return self.get_json(self.USER_DATA_URL, params=params)[0] # get_json returns a list, caller `do_auth()` needs dict

    def get_user_details(self, response):
        print repr(response)
        return {
                'username': response['username'],
                'email': response['email'],
                'first_name': response['first_name'],
                'last_name': response['last_name']
                }
