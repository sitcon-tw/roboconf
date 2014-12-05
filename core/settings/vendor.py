# -*- coding: utf-8 -*-
import datetime

ALLOWED_HOSTS = ['staff.sitcon.org']
SITE_URL = 'https://staff.sitcon.org'

DEFAULT_FROM_EMAIL = u'"SITCON 行政系統" <admin@staff.sitcon.org>'
SERVER_EMAIL = DEFAULT_FROM_EMAIL

DEFAULT_NOTIFICATION_SENDER = u'SITCON 行政系統:notifications@staff.sitcon.org'
DEFAULT_ACCOUNTS_SENDER =  u'SITCON 行政系統:accounts@staff.sitcon.org'
DEFAULT_ISSUE_SENDER = u'SITCON 行政系統:issues@staff.sitcon.org'

SUBMITTER_ACCOUNTS_SENDER = u'SITCON:accounts@staff.sitcon.org'
USER_ISSUE_SENDER = u'{0} (SITCON):issues@staff.sitcon.org'

DEFAULT_SMS_SENDER = 'SITCON'

SUBMISSION_START = datetime.datetime(2014, 12, 5, 12, 0, 0)
SUBMISSION_END = datetime.datetime(2015, 1, 31, 6, 38, 0)
SUBMISSION_RULE_DOCID = 'MUY'

ISSUE_EXPIRE_TIMEDELTA = datetime.timedelta(hours=12)
