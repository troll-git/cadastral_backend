# Generated by Django 3.1.2 on 2020-11-07 00:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0045_auto_20201107_0038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipdata',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
    ]