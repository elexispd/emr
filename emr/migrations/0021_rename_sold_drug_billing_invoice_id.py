# Generated by Django 5.0.1 on 2024-02-21 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0020_rename_invoice_id_billing_sold_drug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billing',
            old_name='sold_drug',
            new_name='invoice_id',
        ),
    ]
