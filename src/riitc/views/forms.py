# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from riitc.contrib.validators import Unique, Exist, Nickname
from riitc.models import AccountModel


class SignupForm(Form):
    nickname = StringField('Nickname',
                           validators=[DataRequired(),
                                       Nickname(),
                                       Unique(AccountModel,
                                              AccountModel.nickname,
                                              message='用户名已被占用')])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email(),
                                    Unique(AccountModel,
                                           AccountModel.email,
                                           message='该邮箱已注册')])
    password = PasswordField('Password', validators=[DataRequired()])


class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class EmailForm(Form):
    email = StringField('Email', validators=[DataRequired(),
                                             Email(),
                                             Exist(AccountModel,
                                                   AccountModel.email,
                                                   message='该邮箱不存在')])


class PasswordForm(Form):
    password = PasswordField('Password', validators=[DataRequired()])
