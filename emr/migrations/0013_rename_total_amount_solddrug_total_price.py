# Generated by Django 5.0.1 on 2024-02-21 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0012_rename_total_price_solddrug_total_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solddrug',
            old_name='total_amount',
            new_name='total_price',
        ),
    ]
