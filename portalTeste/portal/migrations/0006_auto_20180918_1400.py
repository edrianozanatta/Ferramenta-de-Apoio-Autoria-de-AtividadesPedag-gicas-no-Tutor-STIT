# Generated by Django 2.1.1 on 2018-09-18 17:00

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20180918_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='dataInicio',
            field=models.DateField(default=datetime.datetime(2018, 9, 18, 17, 0, 47, 349587, tzinfo=utc)),
        ),
    ]
