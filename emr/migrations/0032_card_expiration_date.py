# Generated by Django 5.0.1 on 2024-03-04 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emr', '0031_billing_is_card_renewal_card_is_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='expiration_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
