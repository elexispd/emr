# Generated by Django 5.0.1 on 2024-02-21 12:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0008_alter_drug_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='SoldDrug',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('drug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='emr.drug')),
            ],
        ),
    ]
