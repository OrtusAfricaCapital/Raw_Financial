# Generated by Django 3.2.5 on 2022-01-27 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0039_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='c66b3bfb47b04e49b9bd3a4d63c63718', editable=False, unique=True),
        ),
    ]