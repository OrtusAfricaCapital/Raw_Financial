# Generated by Django 3.2.5 on 2021-11-25 21:59

import borrowers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('borrowers', '0002_borrower_tn'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='borrower_id',
            field=models.CharField(default=borrowers.models.borrower_rand, editable=False, max_length=20),
        ),
    ]