# Generated by Django 3.2.5 on 2021-11-30 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trust_network', '0003_auto_20211123_1006'),
        ('borrowers', '0006_rename_channel_borrower_id_borrower_channel_borrower_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrower',
            name='tn',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='trust_network.trustnetwork'),
        ),
    ]
