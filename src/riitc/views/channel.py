# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import request, views, redirect, url_for, render_template
from flask.ext.paginate import Pagination
from riitc.blueprints import blueprint_www

from riitc.models import ChannelModel, LevelModel


article_per_page = 10
STAFF_MAPPING = {2: 1, 16: 1, 17: 2, 18: 3, 19: 4, 20: 5, 21: 6}


class ChannelView(views.MethodView):
    '''
        频道页
    '''
    @property
    def page(self):
        try:
            return int(request.args.get('page', 1))
        except ValueError:
            return 1

    @property
    def language(self):
        return request.args.get('lang', 'cn')

    def get(self, cid):
        if cid in STAFF_MAPPING.keys():
            return redirect(url_for('views.staff', cid=cid))
        channel = ChannelModel.query.get(cid)
        query = ChannelModel.get_channel_query(self.language)
        pager = Pagination(bs_version=3, page=self.page,
                           total=channel.articles.count())

        return render_template('www/channel.html',
                               channels=query.all(),
                               channel=channel,
                               language=channel.language,
                               pager=pager)


blueprint_www.add_url_rule('/channel/<int:cid>/',
                           view_func=ChannelView.as_view(b'channel'),
                           endpoint='channel', methods=['GET'])


class LevelView(views.MethodView):
    '''
        师资队伍
    '''

    @property
    def page(self):
        try:
            return int(request.args.get('page', 1))
        except ValueError:
            return 1

    @property
    def language(self):
        return request.args.get('lang', 'cn')

    def get(self, cid):
        channel = ChannelModel.query.get(cid)
        level_id = STAFF_MAPPING.get(cid, None)
        if not level_id:
            return redirect(url_for('views.channel', cid=cid))
        level = LevelModel.query.get(level_id)

        query = ChannelModel.get_channel_query(self.language)
        pager = Pagination(bs_version=3, page=self.page,
                           total=level.all_staff.count())

        return render_template('www/staff.html',
                               channels=query.all(),
                               channel=channel,
                               language=channel.language,
                               pager=pager)


blueprint_www.add_url_rule('/staff/<int:cid>/',
                           view_func=LevelView.as_view(b'level'),
                           endpoint='level', methods=['GET'])
