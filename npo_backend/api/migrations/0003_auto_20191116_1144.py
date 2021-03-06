# Generated by Django 2.2.7 on 2019-11-16 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20191112_1312'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='users_registered',
            field=models.ManyToManyField(related_name='users_registered', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='event_created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
