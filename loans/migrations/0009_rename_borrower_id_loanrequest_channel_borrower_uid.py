# Generated by Django 3.2.5 on 2021-11-30 09:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0008_loanrequeststatus'),
    ]

    operations = [
        migrations.RenameField(
            model_name='loanrequest',
            old_name='borrower_id',
            new_name='channel_borrower_uid',
        ),
    ]
