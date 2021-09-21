# Generated by Django 3.2.5 on 2021-08-30 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trust_network', '0002_alter_trustnetwork_logo'),
        ('borrowers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrower',
            name='tn',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='trust_network.trustnetwork'),
            preserve_default=False,
        ),
    ]
