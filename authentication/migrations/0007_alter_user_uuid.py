# Generated by Django 3.2.5 on 2021-11-29 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='67763edd99e64e8e92360851a273b12c', editable=False, unique=True),
        ),
    ]
