# Generated by Django 3.2.5 on 2021-11-30 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='8faa5f6eecf440cc940eddf15465e0f7', editable=False, unique=True),
        ),
    ]
