# Generated by Django 3.1.1 on 2020-09-30 21:05

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polyserver_api', '0007_auto_20200926_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='PozwoleniaGeom',
            fields=[
                ('pozwolenia_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='polyserver_api.pozwolenia')),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            bases=('polyserver_api.pozwolenia',),
        ),
        migrations.RenameField(
            model_name='pozwolenia',
            old_name='kod_dzialki',
            new_name='identyfikator',
        ),
    ]