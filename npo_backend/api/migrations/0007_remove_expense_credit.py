# Generated by Django 2.2.7 on 2019-11-20 09:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_merge_20191119_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expense',
            name='credit',
        ),
    ]