# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-02-06 22:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_profile', '0005_auto_20170205_0438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nmhwprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='profile_imgs'),
        ),
    ]
