# Generated by Django 3.2.5 on 2021-11-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='dc3b853ebd0a4267a0586d965607f14d', editable=False, unique=True),
        ),
    ]
