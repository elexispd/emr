# Generated by Django 5.0.1 on 2024-02-21 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0011_remove_solddrug_total_solddrug_total_price_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='solddrug',
            old_name='total_price',
            new_name='total_amount',
        ),
    ]