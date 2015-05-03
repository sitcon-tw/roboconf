# -*- coding: utf-8 -*-
import datetime

ALLOWED_HOSTS = ['staff.sitcon.camp']
SITE_URL = 'http://staff.sitcon.camp'

DEFAULT_FROM_EMAIL = u'"SITCON 夏令營行政系統" <admin@staff.sitcon.camp>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

DEFAULT_NOTIFICATION_SENDER = u'SITCON 夏令營行政系統:notifications@staff.sitcon.camp'
DEFAULT_ACCOUNTS_SENDER =  u'SITCON 夏令營行政系統:accounts@staff.sitcon.camp'
DEFAULT_ISSUE_SENDER = u'SITCON 夏令營行政系統:issues@staff.sitcon.camp'

USER_ISSUE_SENDER = u'{0} (SITCON):issues@staff.sitcon.camp'

DEFAULT_SMS_SENDER = 'SITCON'

ISSUE_EXPIRE_TIMEDELTA = datetime.timedelta(hours=12)
