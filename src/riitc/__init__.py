#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.babelex import Babel
from studio.core.flask.app import StudioFlask


app = StudioFlask(__name__)

Babel(app=app, default_locale='zh')

with app.app_context():
    from riitc.contrib import template_filter as tf
    from riitc.contrib.image import thumbnail
    app.jinja_env.globals.update(render_navi=tf.render_navi,
                                 render_activity=tf.render_activity,
                                 render_news=tf.render_news,
                                 thumbnail=thumbnail)
    from riitc import views
    from riitc.panel import admin
    from riitc.blueprints import blueprint_www
    from riitc.contrib.security import login_manager
    admin.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "views.login"
    assert views

    app.register_blueprint(blueprint_www)
    app.add_url_rule('/apps/%s/<path:filename>' %
                     app.name, endpoint='static', #subdomain='static',
                     view_func=app.send_static_file)
