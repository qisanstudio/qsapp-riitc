# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itsdangerous import URLSafeTimedSerializer

from .. import app

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])
