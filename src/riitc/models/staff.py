#! -*- coding: utf-8 -*-
from __future__ import unicode_literals

from studio.core.engines import db
from sqlalchemy.ext.hybrid import hybrid_property


__all__ = [
    'LevelModel',
    'StaffModel',
]


class LevelModel(db.Model):
    __tablename__ = 'level'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    title = db.Column(db.Unicode(256), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    all_staff = db.relationship(
        'StaffModel',
        primaryjoin='LevelModel.id==StaffModel.level_id',
        order_by='StaffModel.date_created',
        foreign_keys='[StaffModel.level_id]',
        backref=db.backref(
            'level', lazy='joined', innerjoin=True),
        passive_deletes='all', lazy='dynamic')

    def __str__(self):
        return self.title


class StaffModel(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer(), nullable=False, primary_key=True)
    level_id = db.Column(db.Integer(), db.ForeignKey('level.id'),
                         nullable=False, index=True)
    name = db.Column(db.Unicode(256), nullable=False)
    avatar = db.Column(db.Unicode(length=2083), nullable=False)
    synopsis = db.Column(db.UnicodeText(), nullable=False)
    info = db.Column(db.MutableDict.as_mutable(db.JSONType()), nullable=True)
    date_created = db.Column(db.DateTime(timezone=True),
                             nullable=False, index=True,
                             server_default=db.func.current_timestamp())

    @hybrid_property
    def paper(self):
        return self.info.get('paper')

    @paper.setter
    def _set_paper(self, value):
        self.info['paper'] = value
