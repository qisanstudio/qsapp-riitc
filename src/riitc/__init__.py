#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask.ext.babelex import Babel
from studio.core.flask.app import StudioFlask


app = StudioFlask(__name__)

Babel(app=app, default_locale='zh')

with app.app_context():
    from riitc.contrib import helpers
    app.jinja_env.globals.update(render_navi=helpers.render_navi,
                                 render_activity=helpers.render_activity,
                                 render_news=helpers.render_news)
    from riitc import views
    from riitc.panel import admin
    from riitc.blueprints import blueprint_www
    admin.init_app(app)
    assert views

    app.register_blueprint(blueprint_www)
    app.add_url_rule('/apps/%s/<path:filename>' %
                     app.name, endpoint='static', #subdomain='static',
                     view_func=app.send_static_file)
