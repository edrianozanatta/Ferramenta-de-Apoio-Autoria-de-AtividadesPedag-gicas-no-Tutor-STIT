# Generated by Django 2.1.1 on 2018-09-29 01:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_auto_20180928_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='dataInicio',
            field=models.DateField(default=datetime.datetime(2018, 9, 29, 1, 19, 27, 856997, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='alternativaA',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='alternativaB',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='alternativaC',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='alternativaD',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='exercicio',
            name='alternativaE',
            field=models.CharField(max_length=300),
        ),
    ]