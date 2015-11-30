# -*- coding: utf-8 -*-

# Copy and rename this file to local_settings.py,
# fill these settings, leave blank if not used, don't delete the lines

# DEVELOPERS: names, secrets and site customizable details should be kept here

from __future__ import unicode_literals
import datetime

SECRET_KEY = 'change this!'

DATABASE_NAME = ''
DATABASE_USER = ''
DATABASE_PASSWORD = ''

ALLOWED_HOSTS = ['*']
SITE_URL = ''

ADMINS = (
    ('SITCON Developers', 'sitcon-dev@googlegroups.com'),
)

MANAGERS = ADMINS

SITE_NAME = 'SITCON 行政系統'
SITE_TITLE = 'SITCON'

EMAIL_HOST = 'localhost'
EMAIL_PORT = '25'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

SMS_API_KEY = ''
SMS_API_SECRET = ''

DEFAULT_SMS_SENDER = 'ROBOCONF'
DEFAULT_SMS_COUNTRY_CODE = '886'    # Taiwan

DEFAULT_FROM_EMAIL = '"SITCON 行政系統" <admin@staff.sitcon.org>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL
BROADCAST_EMAIL = 'sitcon@googlegroups.com'

DEFAULT_NOTIFICATION_SENDER = 'SITCON 行政系統:notifications@staff.sitcon.org'
DEFAULT_ACCOUNTS_SENDER =  'SITCON 行政系統:accounts@staff.sitcon.org'
DEFAULT_ISSUE_SENDER = 'SITCON 行政系統:issues@staff.sitcon.org'

USER_ISSUE_SENDER = '{0} (SITCON):issues@staff.sitcon.org'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.security.DisallowedHost': {
            'handlers': ['file'],
            'propagate': False,
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler'
        },
        'file': {
            'level': 'DEBUG',
            'filename': 'roboconf.log',
            'formatter': 'verbose',
            'class': 'logging.FileHandler'
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(module)s %(process)d %(thread)d %(message)s'
        }
    },
}

STAFF_GROUP_NAME = '工作人員'
STAFF_GROUP_ID = 1

URGENT_ISSUE_ID = 2

GROUP_PRIORITY = [3, 1, 6, 7, 5, 8, 4, 9, 2, 14, 19, 20, 15, 13, 18, 12, 11, 10]    # Sort by team lead -> staff -> consultant

RESIDENCE_OPTIONS = (
    '基隆市', '臺北市', '新北市', '桃園市',
    '新竹市', '新竹縣', '苗栗縣', '臺中市',
    '彰化縣', '南投縣', '雲林縣', '嘉義市',
    '嘉義縣', '臺南市', '高雄市', '屏東縣',
    '臺東縣', '花蓮縣', '宜蘭縣', '澎湖縣',
    '金門縣', '連江縣', '國外',
)

SHIRT_SIZE_OPTIONS = (
    'XS', 'S', 'M', 'L', 'XL', '2XL',
)

DIET_OPTIONS = (
    '葷',
    '忌牛肉', '忌豬肉', '忌海鮮',
    '方便素', '蛋奶素', '全素',
)
