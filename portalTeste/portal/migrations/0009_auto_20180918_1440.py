# Generated by Django 2.1.1 on 2018-09-18 17:40

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_auto_20180918_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='dataInicio',
            field=models.DateField(default=datetime.datetime(2018, 9, 18, 17, 40, 58, 818415, tzinfo=utc)),
        ),
    ]
