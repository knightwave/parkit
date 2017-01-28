# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ParkPerson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phone', models.CharField(max_length=25, blank=True)),
                ('user', models.OneToOneField(related_name='+', null=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'park_person',
            },
            bases=(models.Model,),
        ),
    ]
