# Generated by Django 3.2.5 on 2022-02-12 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0016_alter_channel_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='ApiKey',
            field=models.UUIDField(default='5465bf87e61648aa92c720192c70ae9d', editable=False),
        ),
    ]