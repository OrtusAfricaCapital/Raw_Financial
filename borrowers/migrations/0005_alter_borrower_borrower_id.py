# Generated by Django 3.2.5 on 2021-11-29 12:58

import borrowers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0004_borrower_channel_borrower_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrower',
            name='borrower_id',
            field=models.CharField(blank=True, default=borrowers.models.borrower_rand, editable=False, max_length=20),
        ),
    ]
