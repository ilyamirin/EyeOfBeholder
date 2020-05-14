# Generated by Django 2.2.12 on 2020-05-13 12:08

import FRS.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DialogUser',
            fields=[
                ('uid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, null=True)),
                ('time_enrolled', models.DateTimeField(null=True)),
                ('photo', models.BinaryField(null=True)),
                ('vector', djongo.models.fields.ArrayField(model_container=FRS.models.PhotoVector)),
                ('organization', models.CharField(max_length=255, null=True)),
                ('position', models.CharField(max_length=255, null=True)),
                ('state', models.CharField(max_length=255, null=True)),
                ('photo_path', models.CharField(max_length=255, null=True)),
                ('coords', djongo.models.fields.ListField(blank=True, default=[], null=True)),
            ],
        ),
    ]
