#! -*- coding: utf-8 -*-

from __future__ import unicode_literals

from flask.ext.bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import sql
from studio.core.engines import db
from sqlalchemy.ext.hybrid import hybrid_property


__all__ = [
    'AccountModel',
]


class AccountModel(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    nickname = db.Column(db.Unicode(256), nullable=True)
    email = db.Column(db.Unicode(1024), nullable=True, index=True)
    email_confirmed = db.Column(db.Boolean(), nullable=False,
                                server_default=sql.false())
    _password = db.Column('password', db.String(length=128), nullable=False)
    info = db.Column(db.MutableDict.as_mutable(db.JSONType()), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, plaintext):
        self._password = generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        check_password_hash(self._password, plaintext)
