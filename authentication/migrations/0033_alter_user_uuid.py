# Generated by Django 3.2.5 on 2022-01-22 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0032_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='6565c599b7c54929816b14dc67dd036d', editable=False, unique=True),
        ),
    ]
