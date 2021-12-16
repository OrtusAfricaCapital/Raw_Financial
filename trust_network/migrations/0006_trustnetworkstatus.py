# Generated by Django 3.2.5 on 2021-12-10 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trust_network', '0005_alter_trustnetwork_trustnetwork_uid'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrustNetworkStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active_status', models.CharField(choices=[('yes', 'yes'), ('no', 'no')], default='yes', max_length=100)),
                ('created_at', models.DateField(auto_now=True)),
                ('tn_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='trust_network.trustnetwork')),
            ],
        ),
    ]