# Generated by Django 3.2.5 on 2022-02-12 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0021_alter_loanrequest_channel_borrower_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='loan_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Issued', 'Issued'), ('Paid', 'Paid'), ('Defaulted', 'Defaulted')], default='Running', max_length=100),
        ),
    ]
