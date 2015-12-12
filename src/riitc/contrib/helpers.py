# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import render_template_string
from jinja2 import Markup
from ..models import NaviModel, ChannelModel, ArticleModel


navi_str1 = '''
	{% for channel in navi.channels %}
		{% if not channel.channels %}
			<li class=""><a href="{{ channel.url }}">{{ channel.name }}</a></li>
		{% else %}
			<li class="dropdown">
				<a href="{{ channel.url }}" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-haspopup="true" aria-expanded="false">{{ channel.name }}<span class="caret"></span></a>
				<ul class="dropdown-menu">
				{% for subchannel in channel.channels %}
					<li><a href="{{ subchannel.url }}">{{ subchannel.name }}</a></li>
				{% endfor %}
				</ul>
			</li>
		{% endif %}
	{% endfor %}
'''

navi_str = '''
	{% for channel in navi.channels %}
        <li role="presentation" class="dropdown">
            <a class="dropdown-toggle" data-toggle="dropdown" href="{{ channel.url }}" role="button" aria-haspopup="true" aria-expanded="false">{{ channel.name }}</a>
			<ul class="dropdown-menu">
			{% for subchannel in channel.channels %}
				<li><a href="{{ subchannel.url }}">{{ subchannel.name }}</a></li>
			{% endfor %}
			</ul>
        </li>
	{% endfor %}
'''


activity_str = '''
	<table id="activity" class="table table-bordered">
	    <tbody>
	        <tr>
	    	    <th scope="row">
	    	    	<div>
		    	    	<h3>活动预告</h3>
		    	    	<a href="{{ url_for('views.channel', cid=channel_id, _external=True) }}">更多&gt;</a>
	    	    	</div>
	    	    </th>
	    	    {% for activity in activities[:4] %}
	        	<td><h4>
	        		<a href="{{ activity.url }}">【{{ activity.date_published|strfdate }}】 {{ activity.title }}</a>
	        	</h4></td>
	        	{% endfor %}
	        </tr>
	    </tbody>
	</table>
'''


news_str = '''
	<div class="panel panel-default">
			<div class="panel-heading" style="font-size: 18px;">{{ channel.name }}</div>
			<ul class="list-group">
				{% for article in channel.articles[:10] %}
				<li class="list-group-item" style="border: 0px;">
					<a href="{{ article.url }}" style="color: black;">{{ article.title|truncate(22, True) }}</a>
				</li>
				{% endfor %}
			</ul>
			<div class="panel-footer" style="background-color: white;border-top: 0px;">
				<div class="pull-right"><a href="{{ channel.url }}" style="color: black;">更多></a></div>
				<div class="clearfix"></div>
			</div>
	</div>
'''

def render_navi(navi_id):
    navi = NaviModel.query.get(1)
    return Markup(render_template_string(navi_str, navi=navi))


def render_activity(channel_id):
	activities = (ArticleModel.query
							  .filter_by(cid=59)
							  .order_by(ArticleModel.date_published.desc())
							  .limit(4)
							  .all())
	return Markup(render_template_string(activity_str, channel_id=channel_id, activities=activities))


def render_news(channel_id):
	channel = ChannelModel.query.get(channel_id)
	return Markup(render_template_string(news_str, channel=channel))