# Generated by Django 3.2.5 on 2022-01-06 09:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0016_alter_loans_loan_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='loans',
            name='loan_uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
