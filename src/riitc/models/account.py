#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask.ext.bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import sql
from flask.ext.login import UserMixin
from studio.core.engines import db
from riitc.contrib.security import login_manager
from sqlalchemy.ext.hybrid import hybrid_property

__all__ = [
    'AccountModel',
    'RoleModel',
]


@login_manager.user_loader
def get_account(account_id):
    return AccountModel.query.get(account_id)


roles_accounts = db.Table('roles_accounts',
                          db.Column('account_id',
                                    db.Integer(),
                                    db.ForeignKey('account.id')),
                          db.Column('role_id',
                                    db.Integer(),
                                    db.ForeignKey('role.id')))


class AccountModel(db.Model, UserMixin):
    __tablename__ = 'account'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    nickname = db.Column(db.Unicode(256), nullable=False, unique=True)
    email = db.Column(db.Unicode(1024), nullable=True, index=True)
    is_email_confirmed = db.Column(db.Boolean(), nullable=False,
                                   server_default=sql.false())
    _password = db.Column('password', db.String(length=128), nullable=False)
    info = db.Column(db.MutableDict.as_mutable(db.JSONType()), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())
    roles = db.relationship('RoleModel', secondary=roles_accounts)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return check_password_hash(self._password, plaintext)

    def is_active(self):
        return self.is_email_confirmed

    def __repr__(self):
        return '%s<%s>' % (self.nickname, self.email)


class RoleModel(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    description = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return self.description or self.name
