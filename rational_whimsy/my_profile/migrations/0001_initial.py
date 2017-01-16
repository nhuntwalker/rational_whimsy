# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-15 03:00
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('blog_images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NMHWProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('linkedin', models.CharField(blank=True, default='', max_length=42)),
                ('github', models.CharField(blank=True, default='', max_length=42)),
                ('twitter', models.CharField(blank=True, default='', max_length=42)),
                ('facebook', models.CharField(blank=True, default='', max_length=42)),
                ('instagram', models.CharField(blank=True, default='', max_length=42)),
                ('description', models.TextField(blank=True, default='', max_length=42)),
                ('photo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='blog_images.Image')),
            ],
        ),
    ]
