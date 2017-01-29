# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0003_auto_20170129_1118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='person',
            field=models.ForeignKey(related_name='bookings', to='person.Person'),
            preserve_default=True,
        ),
    ]
