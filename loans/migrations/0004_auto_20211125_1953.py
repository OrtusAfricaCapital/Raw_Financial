# Generated by Django 3.2.5 on 2021-11-25 19:53

from django.db import migrations, models
import django.db.models.deletion
import loans.models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0003_auto_20211125_1202'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='loan_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='loans.loans'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='payment',
            name='payment_id',
            field=models.CharField(default=loans.models.payment_rand, max_length=20),
        ),
    ]
