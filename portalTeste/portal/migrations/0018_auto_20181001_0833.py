# Generated by Django 2.1.1 on 2018-10-01 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_auto_20181001_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercicio',
            name='nome',
            field=models.CharField(max_length=20),
        ),
    ]
