# Generated by Django 2.1.1 on 2018-09-18 18:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0009_auto_20180918_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='dataInicio',
            field=models.DateField(default=datetime.datetime(2018, 9, 18, 18, 20, 51, 673767, tzinfo=utc)),
        ),
    ]
