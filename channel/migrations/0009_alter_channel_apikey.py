# Generated by Django 3.2.5 on 2022-01-22 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0008_alter_channel_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='ApiKey',
            field=models.UUIDField(default='dea6eb68dc534c1ab4223fdd3b64bdab', editable=False),
        ),
    ]