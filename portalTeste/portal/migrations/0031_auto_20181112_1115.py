# Generated by Django 2.1.1 on 2018-11-12 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0030_auto_20181112_1046'),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=85)),
                ('sequence', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ModuleCurriculum',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curriculum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Curriculum')),
                ('module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Module')),
            ],
        ),
        migrations.RemoveField(
            model_name='structurecurriculum',
            name='curriculum',
        ),
        migrations.RemoveField(
            model_name='structurecurriculum',
            name='structure',
        ),
        migrations.DeleteModel(
            name='Structure',
        ),
        migrations.DeleteModel(
            name='StructureCurriculum',
        ),
    ]
