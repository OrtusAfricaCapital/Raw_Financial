# Generated by Django 3.2.5 on 2022-02-12 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0045_alter_user_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default='85370c384bc54f10bb547cb253a91cc5', editable=False, unique=True),
        ),
    ]
