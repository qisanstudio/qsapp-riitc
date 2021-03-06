# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from wtforms import validators
from jinja2 import Markup
from studio.core.engines import db

from riitc.contrib.fields import ImageUploadField
from riitc.contrib.image import thumbnail
from riitc.models import SlideModel, ArticleModel
from .base import BaseView
from .forms import CKTextAreaField


class Article(BaseView):

    create_template = 'panel/article_edit.html'
    edit_template = 'panel/article_edit.html'
    column_labels = {'id': 'ID',
                     'title': '标题',
                     'is_sticky': '置顶',
                     'channel': '频道',
                     'date_published': '发布时间',
                     'date_created': '创建时间'}
    column_list = ['id', 'channel', 'is_sticky', 'title',
                   'date_published', 'date_created']
    column_searchable_list = ['title', ]
    column_default_sort = ('date_published', True)
    form_extra_fields = {
        'content': CKTextAreaField('内容',
                                   validators=[validators.Required()]),
    }

    def __init__(self, **kwargs):
        super(Article, self).__init__(ArticleModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Article, self).create_form()
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Article, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form


class Slide(BaseView):
    column_labels = {'id': 'ID',
                     'order': '排序',
                     'title': '标题',
                     'describe': '描述',
                     'image': '图片链接',
                     'link': '链接',
                     'date_created': '创建时间'}
    column_list = ['id', 'order', 'title', 'describe',
                   'image', 'link', 'date_created']
    column_default_sort = ('order', True)
    form_args = {
        'image': {'label': '图片', 'validators': [validators.Required(),
                                                 validators.URL()]},
        'link': {'label': '链接', 'validators': [validators.Required(),
                                               validators.URL()]},
    }

    def _show_image(self, context, model, name):
        image = model.image.strip() if model.image else ''
        origin_url = thumbnail(image)
        url = thumbnail(image, width=200, height=200)
        return Markup('<a href="%s" target="_blank"><img src="%s" /></a>' % (origin_url, url))

    column_formatters = {
        'image': _show_image,
    }

    form_extra_fields = {
        'image': ImageUploadField('图片上传')
    }

    def __init__(self, **kwargs):
        super(Slide, self).__init__(SlideModel, db.session, **kwargs)

    def create_form(self, obj=None):
        form = super(Slide, self).create_form()
        delattr(form, 'date_created')
        return form

    def edit_form(self, obj=None):
        form = super(Slide, self).edit_form(obj=obj)
        delattr(form, 'date_created')
        return form
