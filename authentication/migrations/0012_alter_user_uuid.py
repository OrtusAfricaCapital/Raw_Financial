# Generated by Django 3.2.5 on 2021-12-06 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='2426a8f46e61426887336550d566fee5', editable=False, unique=True),
        ),
    ]
