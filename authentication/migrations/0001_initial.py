# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-27 17:07
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CountryCodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('authy_status', models.CharField(choices=[('unverified', 'unverified'), ('onetouch', 'onetouch'), ('sms', 'sms'), ('token', 'token'), ('approved', 'approved'), ('denied', 'denied')], default='unverified', max_length=10)),
                ('phone_number', models.CharField(max_length=100, null=True)),
                ('country_code', models.IntegerField(null=True)),
                ('authy_id', models.IntegerField(null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
