# Generated by Django 3.2.5 on 2022-01-26 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0012_alter_channel_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='ApiKey',
            field=models.UUIDField(default='0fc6f656b08d4a7faadd06c46197cc26', editable=False),
        ),
    ]