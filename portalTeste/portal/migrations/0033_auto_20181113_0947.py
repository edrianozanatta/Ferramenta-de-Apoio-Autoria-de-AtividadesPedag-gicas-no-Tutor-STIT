# Generated by Django 2.1.1 on 2018-11-13 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0032_auto_20181113_0944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='difficulty',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)]),
        ),
        migrations.AlterField(
            model_name='instruction',
            name='level',
            field=models.IntegerField(choices=[(1, 1), (2, 2), (3, 3)]),
        ),
    ]
