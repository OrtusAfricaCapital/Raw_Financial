# Generated by Django 3.2.5 on 2022-01-17 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0026_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='67007d0b70a94fb38cf3b8d554d9934c', editable=False, unique=True),
        ),
    ]
