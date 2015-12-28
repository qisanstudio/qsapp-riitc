# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .account import Account, Role
from .channel import Navi, Channel
from .article import Slide, Article
from .staff import Level, Staff
from .image import Image


from flask.ext.admin import Admin


admin = Admin(name='后台管理', url='/admin')

# 账户管理
admin.add_view(Account(name='用户', category='账户管理', endpoint='account'))
admin.add_view(Role(name='角色', category='账户管理', endpoint='role'))

# 频道管理
admin.add_view(Navi(name='导航栏', category='频道管理', endpoint='navi'))
admin.add_view(Channel(name='频道项', category='频道管理', endpoint='channel'))


# 文章管理
admin.add_view(Slide(name='幻灯片', category='文章管理', endpoint='slide'))
admin.add_view(Article(name='文章', category='文章管理', endpoint='article'))


# 职工管理
admin.add_view(Level(name='职称', category='师资队伍', endpoint='level'))
admin.add_view(Staff(name='职员', category='师资队伍', endpoint='staff'))


# 图片管理
admin.add_view(Image(name='图片管理', category='图片管理', endpoint='image'))
