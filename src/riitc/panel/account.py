# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from studio.core.engines import db

from riitc.models import AccountModel, RoleModel
from .base import BaseView


class Account(BaseView):

    can_create = False
    column_labels = {'id': 'ID',
                     'nickname': '昵称',
                     'email': '邮件',
                     'is_email_confirmed': '邮箱验证',
                     'roles': '角色',
                     'date_created': '创建时间'}
    column_list = ['id', 'nickname', 'email',
                   'is_email_confirmed', 'roles', 'date_created']
    column_searchable_list = ['nickname', ]
    column_default_sort = ('date_created', True)

    def __init__(self, **kwargs):
        super(Account, self).__init__(AccountModel, db.session, **kwargs)

    def edit_form(self, obj=None):
        form = super(Account, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        delattr(form, 'nickname')
        delattr(form, 'email')
        delattr(form, 'is_email_confirmed')
        return form


class Role(BaseView):

    column_labels = {'id': 'ID',
                     'name': '名称',
                     'description ': '描述'}

    def __init__(self, **kwargs):
        super(Role, self).__init__(RoleModel, db.session, **kwargs)
