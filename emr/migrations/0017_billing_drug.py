# Generated by Django 5.0.1 on 2024-02-21 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0016_solddrug_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='drug',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='emr.solddrug'),
        ),
    ]
