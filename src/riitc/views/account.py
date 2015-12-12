# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, views, render_template

from studio.core.engines import db
from riitc.blueprints import blueprint_www
from riitc.models import AccountModel


class RegisterView(views.MethodView):
    '''
        注册用户
    '''

    def post(self):
        AccountModel
        return render_template('www/register.html')


blueprint_www.add_url_rule('/register', view_func=RegisterView.as_view(b'register'),
                           endpoint='register', methods=['POST'])
