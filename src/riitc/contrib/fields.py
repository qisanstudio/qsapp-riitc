# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import qiniu

from flask import flash
from flask_admin import form

from riitc.contrib.image import qn, calc_hashkey
from .. import app


class ImageUploadField(form.ImageUploadField):

    def _save_file(self, f, _):
        hashkey = calc_hashkey(f)
        token = qn.upload_token(app.config['QINIU_IMAGE_BUCKET'], hashkey)
        f.seek(0)
        ret, _ = qiniu.put_data(token, hashkey, f, mime_type='image/jpeg')
        if ret is not None:
            flash('上传成功')

        return hashkey
