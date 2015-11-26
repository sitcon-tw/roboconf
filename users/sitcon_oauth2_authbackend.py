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
    SCOPE_SEPARATOR = ','
    AUTHORIZATION_URL = settings.SITCON_OAUTH2_AUTHORIZATION_URL
    ACCESS_TOKEN_URL = settings.SITCON_OAUTH2_ACCESS_TOKEN_URL
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = settings.SITCON_OAUTH2_REVOKE_TOKEN_URL
    REVOKE_TOKEN_METHOD = 'DELETE'
    USER_DATA_URL = settings.SITCON_OAUTH2_USER_DATA_URL
    EXTRA_DATA = []
