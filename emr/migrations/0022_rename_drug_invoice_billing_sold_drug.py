# Generated by Django 5.0.1 on 2024-02-21 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0021_rename_sold_drug_billing_invoice_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billing',
            old_name='drug_invoice',
            new_name='sold_drug',
        ),
    ]
