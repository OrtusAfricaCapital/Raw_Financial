# Generated by Django 3.2.5 on 2021-09-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletwithdraw',
            name='withdrew_on',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
