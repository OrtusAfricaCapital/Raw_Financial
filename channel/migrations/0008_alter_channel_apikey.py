# Generated by Django 3.2.5 on 2022-01-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channel', '0007_alter_channel_apikey'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='ApiKey',
            field=models.UUIDField(default='79e6ed5088014121be35c12688ebdd6a', editable=False),
        ),
    ]
