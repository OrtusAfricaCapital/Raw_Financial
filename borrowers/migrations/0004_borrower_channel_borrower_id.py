# Generated by Django 3.2.5 on 2021-11-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0003_borrower_borrower_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='channel_borrower_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]