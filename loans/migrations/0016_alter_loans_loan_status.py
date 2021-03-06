# Generated by Django 3.2.5 on 2022-01-06 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0015_loans_loan_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loans',
            name='loan_status',
            field=models.CharField(choices=[('Issued', 'Issued'), ('Running', 'Running'), ('Paid', 'Paid'), ('Defaulted', 'Defaulted')], default='Running', max_length=100),
        ),
    ]
