# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20150805_2221'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='img_url',
            field=models.TextField(default=''),
            preserve_default=True,
        ),
    ]
