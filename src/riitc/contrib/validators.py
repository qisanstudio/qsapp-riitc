# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms.validators import Regexp, ValidationError


class Unique(object):
    def __init__(self, model, field, message=u'已存在'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)


class Exist(object):
    def __init__(self, model, field, message=u'不存在'):
        self.model = model
        self.field = field
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if not check:
            raise ValidationError(self.message)


class Nickname(Regexp):
    def __init__(self, message=None):
        super(Nickname, self).__init__(
            ur'[\w\u3400-\u4db5\u4e00-\u9fcb.-]{1,20}', message=message)

    def __call__(self, form, field):
        if self.message is None:
            self.message = '昵称仅限中英文、数字、“.”、“-”及“_”'
        super(Nickname, self).__call__(form, field)
