# Generated by Django 3.2.5 on 2022-01-22 12:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0005_alter_channel_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='ApiKey',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]