# Generated by Django 3.2.5 on 2022-02-12 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0040_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='d91d103849444861982b5837708deac7', editable=False, unique=True),
        ),
    ]