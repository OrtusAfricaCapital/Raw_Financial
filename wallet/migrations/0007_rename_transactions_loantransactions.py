# Generated by Django 3.2.5 on 2022-01-16 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0017_loans_loan_uid'),
        ('wallet', '0006_transactions'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transactions',
            new_name='LoanTransactions',
        ),
    ]
