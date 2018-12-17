# Generated by Django 2.1.1 on 2018-10-12 12:53

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0019_auto_20181004_1152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exercicio',
            name='aula',
        ),
        migrations.AlterField(
            model_name='activity',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500),
        ),
        migrations.AlterField(
            model_name='alternative',
            name='answer',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500),
        ),
        migrations.AlterField(
            model_name='step',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(max_length=500),
        ),
        migrations.DeleteModel(
            name='Aula',
        ),
        migrations.DeleteModel(
            name='Exercicio',
        ),
    ]
