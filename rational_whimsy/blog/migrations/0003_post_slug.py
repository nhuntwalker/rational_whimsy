# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.SlugField(default='none', max_length=255),
            preserve_default=False,
        ),
    ]
