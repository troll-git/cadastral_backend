# Generated by Django 3.1.2 on 2020-11-07 00:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0044_ipdata'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ipdata',
            old_name='Ipv4',
            new_name='IPv4',
        ),
    ]
