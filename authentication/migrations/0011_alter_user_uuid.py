# Generated by Django 3.2.5 on 2021-12-04 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0010_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='3adb6aa140914a2fb2d26df0c3beba1d', editable=False, unique=True),
        ),
    ]