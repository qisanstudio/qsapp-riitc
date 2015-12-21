# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms import validators
from jinja2 import Markup
from studio.core.engines import db

from riitc.models import LevelModel, StaffModel
# from .forms import CKTextAreaField
from .base import BaseView


class Level(BaseView):

    column_labels = {'id': 'ID',
                     'title': '职位',
                     'date_created': '创建时间'}
    column_list = ['id', 'title', 'date_created']
    # column_default_sort = ('date_published', True)

    def __init__(self, **kwargs):
        super(Level, self).__init__(LevelModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Level, self).create_form()
        delattr(form, 'date_created')
        delattr(form, 'all_staff')
        return form

    def edit_form(self, obj=None):
        form = super(Level, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        delattr(form, 'all_staff')
        return form


class Staff(BaseView):
    column_labels = {'id': 'ID',
                     'name': '名字',
                     'avatar': '头像',
                     'synopsis': '综述',
                     'level': '职位',
                     'date_created': '创建时间'}
    column_list = ['id', 'name', 'avatar', 'synopsis', 'date_created']
    column_default_sort = ('date_created', True)
    form_args = {
        'avatar': {'label': '头像', 'validators': [validators.Required(),
                                                 validators.URL()]},
    }

    def _show_avatar(self, context, model, name):
        avatar = model.avatar.strip() if model.avatar else ''
        return Markup('<img src=%s width=200 height=200 />' % avatar)

    column_formatters = {
        'avatar': _show_avatar,
    }

    def __init__(self, **kwargs):
        super(Staff, self).__init__(StaffModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Staff, self).create_form()
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Staff, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form
