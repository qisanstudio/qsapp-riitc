# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
from flask import request, views, redirect, url_for, render_template

from riitc.contrib.security import requires_roles
from studio.core.engines import db
from riitc.blueprints import blueprint_www
from riitc.models import (SlideModel, ChannelModel, ChannelSummaryModel,
                          ArticleModel, ArticleContentModel)


class IndexView(views.MethodView):
    '''
        首页
    '''

    @requires_roles('superadmin')
    def get(self):
        return redirect(url_for('views.index_lang', language='cn'))


blueprint_www.add_url_rule('/', view_func=IndexView.as_view(b'index'),
                           endpoint='index', methods=['GET'])


class LangIndexView(views.MethodView):
    '''
        语言首页
    '''

    def get(self, language):
        channels = ChannelModel.query.all()
        if language == 'en':
            channels = filter(lambda x: re.match(r'[a-zA-Z\b]+', x.name),
                              channels)
        else:
            channels = filter(lambda x: not re.match(r'[a-zA-Z\b]+', x.name),
                              channels)
        slides = SlideModel.query.order_by(SlideModel.order).all()
        return render_template('www/index.html',
                               slides=slides,
                               channels=channels,
                               language=language)


blueprint_www.add_url_rule('/l/<language>/',
                           view_func=LangIndexView.as_view(b'index_lang'),
                           endpoint='index_lang', methods=['GET'])


class SearchView(views.MethodView):
    '''
        搜索
    '''

    def _search(self, kw):
        channels = (ChannelModel.query
                                .join('_summary')
                                .filter(db.or_(ChannelModel.name.like('%'+kw+'%'),
                                               ChannelSummaryModel.content.like('%'+kw+'%')))
                                .all())
        articles = (ArticleModel.query
                                .join('_content')
                                .filter(db.or_(ArticleModel.title.like('%'+kw+'%'),
                                               ArticleContentModel.content.like('%'+kw+'%')))
                                .all())

        return channels+articles

    def get(self, category):
        kw = request.args.get('kw', '')
        result = self._search(kw) if kw else []
        return render_template('www/search.html', kw=kw, result=result)

blueprint_www.add_url_rule('/search/<category>/',
                            view_func=SearchView.as_view(b'search'),
                            endpoint='search', methods=['GET'])
