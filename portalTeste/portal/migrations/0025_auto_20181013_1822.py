# Generated by Django 2.1.1 on 2018-10-13 21:22

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0024_auto_20181013_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternative',
            name='answer_ckeditor',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, max_length=500, null=True),
        ),
    ]
