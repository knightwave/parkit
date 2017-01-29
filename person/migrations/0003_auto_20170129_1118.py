# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('person', '0002_auto_20170128_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startTime', models.DateTimeField()),
                ('endTime', models.DateTimeField()),
                ('isActive', models.BooleanField(default=True)),
                ('cost', models.DecimalField(default=0.0, max_digits=4, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ParkingSpot',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('latitude', models.CharField(max_length=20)),
                ('longitude', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=254)),
                ('maxTime', models.PositiveIntegerField(default=300, null=True)),
                ('minTime', models.PositiveIntegerField(default=30, null=True)),
                ('totalSpots', models.IntegerField(default=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='booking',
            name='parkingSpot',
            field=models.ForeignKey(related_name='bookings', to='person.ParkingSpot'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking',
            name='person',
            field=models.ForeignKey(related_name='bookings', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
